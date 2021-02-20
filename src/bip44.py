import struct
from binascii import unhexlify
from base58 import b58encode_check
from src.secp256k1 import secp256k1, CurvePoint
from src.bip32 import BIP32_Account

endianness = 'big'

class BIP44(BIP32_Account):
	def __init__(self, seed):
		super().__init__(seed)
		self.prv_version = b'\x04\x88\xAD\xE4'
		self.pub_version = b'\x04\x88\xB2\x1E'
		self.master_prv, self.master_pub = self.derive_master_keys()

	def derive_master_keys(self):
		''' Generate a master extended key pair '''
		depth = b'\x00'
		# set master key index (0x00) and master key fingerprint (0x00000000)
		m_id = b'\x00' * 4
		# generate the extended key pair
		return self.gen_prv(depth, m_id, m_id, self.master_prv, self.master_chain), self.gen_pub(depth, m_id, m_id, self.master_prv, self.master_chain)

	def get_master_keys(self):
		''' Return the master xkeys '''
		return self.master_prv, self.master_pub

	def gen_prv(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the private key from a BIP39 seed '''
		print(f'PRV: \n{depth}\n{fingerprint}\n{index}\n{prvkey}\n{chaincode}')
		xprv = self.prv_version + depth + fingerprint + index + chaincode + b'\x00' + prvkey
		return b58encode_check(xprv).decode()

	def gen_pub(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the public key by multiplying the private key by the secp256k1 base point '''
		print(f'PUB: \n{depth}\n{fingerprint}\n{index}\n{prvkey}\n{chaincode}')
		pubkey = self.point(prvkey)
		try:
			# compress the public key's y coordinate
			pubkey = self.compress_pubkey(pubkey)
		except ValueError as v:
			print(f'Error: {v}')
		# generate and return an xpub key encoded with base58check
		xpub = self.pub_version + depth + fingerprint + index + chaincode + pubkey
		return b58encode_check(xpub).decode()
	
	def derive_child_keys(self, xprv, xpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.derive_child_prvkey(xprv, xpub, depth, index)
		# generate child extended public key
		child_pub = self.derive_child_pubkey(child_prv, xpub, depth, index)
		return child_prv, child_pub
	
	def derive_child_prvkey(self, xprv, xpub, depth, index):
		# extract private, public, and chain code
		prv, chain = self.extract_prv(xprv)
		pub = self.extract_pub(xpub)
		# generate the private child key
		child = self.ckd_prv(prv, chain, index)
		# split the private key and chain code
		child_prv, child_chain = self.split_childkey(child)
		# generate the fingerprint for the key
		fingerprint = self.generate_fingerprint(pub)
		# generate child private key
		child_prv = (int(child_prv, 16) + int(prv.hex(), 16)) % secp256k1().n
		#FIXME: check if derived key is valid
		child_yprv = self.prv_version + depth + fingerprint + index + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(32, endianness)
		return b58encode_check(child_yprv).decode()

	def derive_child_pubkey(self, child_prv, parent_pub, depth, index):
		''' Generate a child public key '''
		# extract child private key and chain code
		child_prv, child_chain = self.extract_prv(child_prv)
		# generate and compress child public key
		child_pub = self.compress_pubkey(self.point(child_prv))
		# generate the parent fingerprint from the public key
		fingerprint = self.generate_fingerprint(self.extract_pub(parent_pub))
		# serialize the child xpub key
		child_ypub = self.pub_version + depth + fingerprint + index + child_chain + child_pub
		# return the child xpub key encoded in bas58_check
		return b58encode_check(child_ypub).decode()
	
	def derive_path(self, path):
		''' Derive a BIP 44 path:
				m/44'/coin_type'/account'/change/address_index
		'''
		path_indices = self.decode_path(path)
		try:
			if len(path_indices) < 5:
				raise ValueError('BIP 44 path `{path_indices}` is not valid')
			#if path_indices[1] != 0x8000002C:
			#	raise ValueError('BIP 44 purpose `{path_indices[1]}` is not valid')
			if not self.is_hardened(path_indices[2]):
				raise ValueError('BIP 44 coin_type `{path_indices[2]}` is not valid')
			if not self.is_hardened(path_indices[3]):
				raise ValueError('BIP 44 account number `{path_indices[3]}` is not valid')
			return self.generate_keypath(path_indices)
		except ValueError as err:
			print(f'Error occurred: {err}.')

	def generate_keypath(self, path_indices):
		''' Generate a BIP wallet chain along a given path '''
		# decode the chain's path
		keypairs = []
		for depth, index in enumerate(path_indices):
			if index == "m":
				# Generate the master extended key pair
				xprv, xpub = self.master_prv, self.master_pub
				print(f'Keys: \n{xprv}\n{xpub}')
			else:
				try:
					# ensure that key index and depth variables do not overflow
					if not (0x00 <= depth <= 0xff):
						raise ValueError(f'Invalid key depth {depth}')
					if not (0x00 <= index <= 0xffffffff):
						raise ValueError(f'Invalid key index {index}')
					# Generate a child extended key pair
					xprv, xpub = self.derive_child_keys(xprv, xpub, depth.to_bytes(1, endianness), index)
				except ValueError as err:
					print(f'Error deriving child key: {err}.')
					return None
			keypairs.append({"prv": xprv, "pub": xpub})
		return keypairs

	def derive_address(self, xpub):
		''' Generate a legacy Bitcoin address '''
		# hash the public key with sha256 and then ripemd160; prepend it with 0x00
		pubkey_hash = b'\x00' + self.hash160(xpub)
		# encode the hash
		return b58encode_check(pubkey_hash).decode()

	def gen_addr_range(self, path, rnge):
		# generate the BIP 44 path down to the 4th level
		keypairs = self.derive_path(path)
		keys = keypairs[-1]
		# extract keys
		m_yprv, m_ypub = keys["prv"], keys["pub"]
		depth = int(5).to_bytes(1, endianness)
		addrs = []
		for i in range(rnge):
			#
			yprv, ypub = self.derive_child_keys(m_yprv, m_ypub, depth, i)
			#
			addrs.append(self.derive_address(self.extract_pub(ypub)))
		return addrs

if __name__ == "__main__":
	rootseed = "67f93560761e20617de26e0cb84f7234aaf373ed2e66295c3d7397e6d7ebe882ea396d5d293808b0defd7edd2babd4c091ad942e6a9351e6d075a29d4df872af"
	path = "m/49'/0'/0'/0"
	wallet = BIP44(rootseed)
	addrs = wallet.gen_addr_range(path, 20)
	for a in addrs:
		print(a)
