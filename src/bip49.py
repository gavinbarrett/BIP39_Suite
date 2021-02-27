import struct
from binascii import unhexlify
from base58 import b58encode_check
from src.bip32 import BIP32_Account
from src.secp256k1 import secp256k1, CurvePoint

endianness = 'big'

class BIP49(BIP32_Account):
	def __init__(self, seed, fromseed=False):
		super().__init__(seed, fromseed)
		# yprivate key version
		self.prv_version = b'\x04\x9d\x78\x78'
		# ypublic key version
		self.pub_version = b'\x04\x9d\x7c\xb2'
		self.master_yprv, self.master_ypub = self.derive_master_keys()
	
	def derive_master_keys(self):
		''' Generate a master extended key pair '''
		depth = b'\x00'
		# set master key index (0x00) and master key fingerprint (0x00000000)
		m_id = b'\x00' * 4
		# generate the extended key pair
		return self.gen_prv(depth, m_id, m_id, self.master_prv, self.master_chain), self.gen_pub(depth, m_id, m_id, self.master_prv, self.master_chain)

	def get_master_keys(self):
		return self.master_yprv, self.master_ypub

	def gen_prv(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the private key from a BIP39 seed '''
		yprv = self.prv_version + depth + fingerprint + index + chaincode + b'\x00' + prvkey
		return b58encode_check(yprv).decode()

	def gen_pub(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the public key by multiplying the private key by the secp256k1 base point '''
		pubkey = self.point(prvkey)
		try:
			# compress the public key's y coordinate
			pubkey = self.compress_pubkey(pubkey)
		except ValueError as v:
			print(f'Error: {v}')
		# generate and return an xpub key encoded with base58check
		ypub = self.pub_version + depth + fingerprint + index + chaincode + pubkey
		return b58encode_check(ypub).decode()
	
	def derive_child_keys(self, yprv, ypub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.derive_child_prvkey(yprv, ypub, depth, index)
		# generate child extended public key
		child_pub = self.derive_child_pubkey(child_prv, ypub, depth, index)
		return child_prv, child_pub
	
	def derive_child_prvkey(self, yprv, ypub, depth, index):
		# extract private, public, and chain code
		prv, chain = self.extract_prv(yprv)
		pub = self.extract_pub(ypub)
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
				yprv, ypub = self.master_yprv, self.master_ypub
			else:
				try:
					# ensure that key index and depth variables do not overflow
					if not (0x00 <= depth <= 0xff):
						raise ValueError(f'Invalid key depth {depth}')
					if not (0x00 <= index <= 0xffffffff):
						raise ValueError(f'Invalid key index {index}')
					# Generate a child extended key pair
					yprv, ypub = self.derive_child_keys(yprv, ypub, depth.to_bytes(1, endianness), index)
				except ValueError as err:
					print(f'Error deriving child key: {err}.')
					return None
			keypairs.append({"prv": yprv, "pub": ypub})
		return keypairs

	def derive_address(self, ypub):
		# generate witness program
		witness = b'\x00\x14' + self.hash160(ypub)
		return b58encode_check(b'\x05' + self.hash160(witness)).decode()

	def gen_addr_range(self, path, rnge, hardened=False):
		# generate the BIP 44 path down to the 4th level
		keypairs = self.derive_path(path)
		keys = keypairs[-1]
		# extract keys
		m_yprv, m_ypub = keys["prv"], keys["pub"]
		depth = int(5).to_bytes(1, endianness)
		addrs = []
		offset = 2**31 if hardened else 0
		for i in range(rnge):
			#
			yprv, ypub = self.derive_child_keys(m_yprv, m_ypub, depth, i + offset)
			#
			addrs.append(self.derive_address(self.extract_pub(ypub)))
		return addrs
