import json
import hmac
import hashlib
import struct
from sys import byteorder, exit
from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac, sha256, sha512
from bip39 import bip39, generate_rootseed
from secp256k1 import secp256k1, CurvePoint
from base58 import b58encode, b58encode_check, b58decode, b58decode_check

# xprivate key version
x_prvkey_v = b'\x04\x88\xAD\xE4'
# xpublic key version
x_pubkey_v = b'\x04\x88\xB2\x1E'
# yprivate key version
y_prvkey_v = b'\x04\x9d\x78\x78'
# ypublic key version
y_pubkey_v = b'\x04\x9d\x7c\xb2'
# zprivate key version
z_prvkey_v = b'\x04\xb2\x43\x0c'
# zpublic key version
z_pubkey_v = b'\x04\xb2\x47\x46'

# set byte endianness
endianness = 'big'



class BIP32_Account:

	def __init__(self, rootseed):
		# Generate BIP 39 root seed
		self.rootseed = unhexlify(rootseed)
		self.rootnode = self.generate_rootkey(self.rootseed)
		self.master_prv, self.master_chain = self.split_rootkey(self.rootnode)
		print(f'Master: {self.master_chain}')

	# FIXME: create valid_key/on_curve function
	def generate_rootkey(self, seed):
		# derive the root key from the BIP39 seed
		return hmac.digest(b'Bitcoin seed', seed, sha512).hex()

	def split_rootkey(self, rootkey):
		# split the root key into a master secret key and a master chain code
		length = len(rootkey) // 2
		master_key, chain_code = rootkey[:length], rootkey[length:]
		if (int(master_key, 16) <= 0) or (int(master_key, 16) >= secp256k1().n):
			raise ValueError("Master key is not valid!")
		return unhexlify(master_key), unhexlify(chain_code)

	def generate_secret(self, rootseed):
		# generate the master node
		key = self.generate_rootkey(rootseed)
		# split the private key from the chain code
		return self.split_rootkey(key)

	def amt_bytes(self, n):
		''' Convert an arbitrary integer into a stream of bytes '''
		if n.bit_length() % 8 == 0:
			return n.bit_length() // 8
		return (n.bit_length() + (8 - (n.bit_length() % 8))) // 8

	def point(self, prv_key):
		# compute the public key: K = k*G
		private = int.from_bytes(prv_key, endianness)
		return secp256k1().generate_pubkey(private)

	def compress_pubkey(self, pubkey):
		# encode the y coordinte in the first byte of the public key
		if pubkey.y & 1:
		#	print(f'Pubkey.x {pubkey.x}\nHex: {hex(pubkey.x)}\nStripped: {hex(pubkey.x)[2:]}')
			return b'\x03' + pubkey.x.to_bytes(32, endianness)
			#return unhexlify('03' + hex(pubkey.x)[2:])
		return b'\x02' + pubkey.x.to_bytes(32, endianness)

	def extract_prv(self, prv):
		''' Extracts a private key and the chain code from an extended private key '''
		decoded = b58decode_check(prv.encode())
		return decoded[-32:], decoded[13:45]

	def extract_pub(self, pub):
		''' Extracts a public key from an extended public key '''
		decoded = b58decode_check(pub.encode())
		return decoded[-33:]

	def split_childkey(self, childkey):
		''' Split the childkey in half '''
		length = len(childkey) // 2
		return childkey[:length], childkey[length:]

	def decode_path(self, path):
		# FIXME: Refactor function
		# m/0'/1/2'/2/1000000000
		args = path.split('/')
		# pop master token `m` from path tokens
		arrs = []
		for a in args:
			idx = None
			if a == "m":
				arrs.append(a)
			elif a[-1] == "'":
				# hardened key
				# strip apostrophe
				a = a[:-1]
				arrs.append(int(a) + 2**31)
			else:
				# non-hardened key
				arrs.append(int(a))
		return arrs

	def hash160(self, pubkey):
		# hash the parent key with sha256
		sha = sha256()
		sha.update(pubkey)
		# hash the digest with ripemd160
		ripemd = hashlib.new('ripemd160')
		ripemd.update(sha.digest())
		return ripemd.digest()

	def wif_encode_prv(self, xprv):
		''' Encrypt a private key in WIF format '''
		# extract private key
		prv, chain = self.extract_prv(xprv)
		# encode private key with WIF codes
		return b58encode_check(b'\x80' + prv + b'\x01')

	def gen_legacy_addr(self, xpub):
		''' Generate a legacy Bitcoin address '''
		# hash the public key with sha256 and then ripemd160; prepend it with 0x00
		pubkey_hash = b'\x00' + self.hash160(xpub)
		# encode the hash
		return b58encode_check(pubkey_hash).decode()

	def generate_fingerprint(self, pubkey):
		''' Return the first four bytes of the hash160 '''
		return self.hash160(pubkey)[:4]

	def hmac_key(self, chain, data):
		# hash a key appended with the index with hmac keyed with the chain code and using sha512
		return hmac.new(chain, data, sha512).hexdigest()

	def is_hardened(self, index):
		''' Return true if a number falls within range of a hardened key index '''
		return 2**31 <= index <= 2**32

	def ckd_prv(self, prv, chain, index):
		''' Derives the child key from the parent private key and chain code
			CKDpriv:
			((k_par, c_par), i) -> (k_i, c_i)
		'''
		if int.from_bytes(index, endianness) >= 0x80000000:
			# child is a hardened key
			key = b'\x00' + prv + index
		else:
			# child is a normal key
			key = self.compress_pubkey(self.point(prv)) + index
		# return the child private key
		return self.hmac_key(chain, key)

	def generate_child_prvkey(self, xprv, xpub, depth, index, version):
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
		child_yprv = version + depth + fingerprint + index + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(32, endianness)
		return b58encode_check(child_yprv).decode()

	def generate_child_pubkey(self, child_prv, parent_pub, depth, index, version):
		''' Generate a child public key '''
		# extract child private key and chain code
		child_prv, child_chain = self.extract_prv(child_prv)
		# generate and compress child public key
		child_pub = self.compress_pubkey(self.point(child_prv))
		# generate the parent fingerprint from the public key
		fingerprint = self.generate_fingerprint(self.extract_pub(parent_pub))
		# serialize the child xpub key
		child_ypub = version + depth + fingerprint + index + child_chain + child_pub
		# return the child xpub key encoded in bas58_check
		return b58encode_check(child_ypub).decode()

	def gen_master_xkeys(self, rootseed):
		''' Generate a master extended key pair '''
		depth = b'\x00'
		# set master key index (0x00) and master key fingerprint (0x00000000)
		m_id = b'\x00' * 4
		# generate a private secret from the rootseed
		prv_key, chain_code = self.generate_secret(rootseed)
		# generate the extended key pair
		return self.gen_xprv(depth, m_id, m_id, prv_key, chain_code), self.gen_xpub(depth, m_id, m_id, prv_key, chain_code)

	def gen_master_ykeys(self, rootseed):
		''' Generate a master extended key pair '''
		depth = b'\x00'
		# set master key index (0x00) and master key fingerprint (0x00000000)
		m_id = b'\x00' * 4
		# generate a private secret from the rootseed
		prv_key, chain_code = self.generate_secret(rootseed)
		# generate the extended key pair
		return self.gen_yprv(depth, m_id, m_id, prv_key, chain_code), self.gen_ypub(depth, m_id, m_id, prv_key, chain_code)

	def gen_xprv(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the private key from a BIP39 seed '''
		xprv = x_prvkey_v + depth + fingerprint + index + chaincode + b'\x00' + prvkey
		return b58encode_check(xprv).decode()

	def gen_xpub(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the public key by multiplying the private key by the secp256k1 base point '''
		pubkey = self.point(prvkey)
		try:
			# compress the public key's y coordinate
			pubkey = self.compress_pubkey(pubkey)
		except ValueError as v:
			print(f'Error: {v}')
		# generate and return an xpub key encoded with base58check
		xpub = x_pubkey_v + depth + fingerprint + index + chaincode + pubkey
		return b58encode_check(xpub).decode()
	
	def gen_yprv(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the private key from a BIP39 seed '''
		yprv = y_prvkey_v + depth + fingerprint + index + chaincode + b'\x00' + prvkey
		return b58encode_check(yprv).decode()

	def gen_ypub(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the public key by multiplying the private key by the secp256k1 base point '''
		pubkey = self.point(prvkey)
		try:
			# compress the public key's y coordinate
			pubkey = self.compress_pubkey(pubkey)
		except ValueError as v:
			print(f'Error: {v}')
		# generate and return an xpub key encoded with base58check
		ypub = y_pubkey_v + depth + fingerprint + index + chaincode + pubkey
		return b58encode_check(ypub).decode()

	def gen_child_xkeys(self, xprv, xpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.generate_child_prvkey(xprv, xpub, depth, index, x_prvkey_v)
		# generate child extended public key
		child_pub = self.generate_child_pubkey(child_prv, xpub, depth, index, x_pubkey_v)
		return child_prv, child_pub
	
	def gen_child_ykeys(self, xprv, xpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.generate_child_prvkey(xprv, xpub, depth, index, y_prvkey_v)
		# generate child extended public key
		child_pub = self.generate_child_pubkey(child_prv, xpub, depth, index, y_pubkey_v)
		return child_prv, child_pub
	
	def gen_child_zkeys(self, xprv, xpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.generate_child_prvkey(xprv, xpub, depth, index, z_prvkey_v)
		# generate child extended public key
		child_pub = self.generate_child_pubkey(child_prv, xpub, depth, index, z_pubkey_v)
		return child_prv, child_pub


	def generate_keypath(self, path_indices):
		''' Generate a BIP wallet chain along a given path '''
		# decode the chain's path
		keypairs = []
		for depth, index in enumerate(path_indices):
			if index == "m":
				# Generate the master extended key pair
				xprv, xpub = self.gen_master_xkeys(unhexlify(self.rootseed))
			else:
				try:
					# ensure that key index and depth variables do not overflow
					if not (0x00 <= depth <= 0xff):
						raise ValueError(f'Invalid key depth {depth}')
					if not (0x00 <= index <= 0xffffffff):
						raise ValueError(f'Invalid key index {index}')
					# Generate a child extended key pair
					xprv, xpub = self.gen_child_xkeys(xprv, xpub, depth.to_bytes(1, endianness), index)
				except ValueError as err:
					print(f'Error deriving child key: {err}.')
					return None
			keypairs.append({"prv": xprv, "pub": xpub})
		return keypairs
	
	def generate_ykeypath(self, path_indices):
		''' Generate a BIP wallet chain along a given path '''
		# decode the chain's path
		keypairs = []
		for depth, index in enumerate(path_indices):
			if index == "m":
				# Generate the master extended key pair
				yprv, ypub = self.gen_master_ykeys(unhexlify(self.rootseed))
			else:
				try:
					# ensure that key index and depth variables do not overflow
					if not (0x00 <= depth <= 0xff):
						raise ValueError(f'Invalid key depth {depth}')
					if not (0x00 <= index <= 0xffffffff):
						raise ValueError(f'Invalid key index {index}')
					# Generate a child extended key pair
					yprv, ypub = self.gen_child_ykeys(yprv, ypub, depth.to_bytes(1, endianness), index)
				except ValueError as err:
					print(f'Error deriving child key: {err}.')
					return None
			keypairs.append({"prv": yprv, "pub": ypub})
		return keypairs

	def gen_addr_range(self, path, rnge):
		# generate the BIP 44 path down to the 4th level
		keypairs = self.gen_bip44_path(path)
		keys = keypairs[-1]
		# extract keys
		m_xprv, m_xpub = keys["prv"], keys["pub"]
		depth = int(5).to_bytes(1, endianness)
		addrs = []
		for i in range(rnge):
			xprv, xpub = self.gen_child_xkeys(m_xprv, m_xpub, depth, i)
			addrs.append(self.gen_legacy_addr(self.extract_pub(xpub)))
			#print(f'add: {self.gen_legacy_addr(self.extract_pub(xpub))}')
			#print(f'pub: {self.extract_pub(xpub).hex()}')
			#print(f'prv: {self.wif_encode_prv(xprv)}\n')
		return addrs

	def gen_bip44_path(self, path):
		''' Derive a BIP 44 path:
				m/44'/coin_type'/account'/change/address_index
		'''
		path_indices = self.decode_path(path)
		try:
			if len(path_indices) < 5:
				raise ValueError('BIP 44 path `{path_indices}` is not valid')
			if path_indices[1] != 0x8000002C:
				raise ValueError('BIP 44 purpose `{path_indices[1]}` is not valid')
			if not self.is_hardened(path_indices[2]):
				raise ValueError('BIP 44 coin_type `{path_indices[2]}` is not valid')
			if not self.is_hardened(path_indices[3]):
				raise ValueError('BIP 44 account number `{path_indices[3]}` is not valid')
			return self.generate_keypath(path_indices)
		except ValueError as err:
			print(f'Error occurred: {err}.')
	
	def gen_bip49_path(self, path):
	#FIXME: define BIP 49 segwit addresses (P2WPKH-P2SH)
		''' Derive a BIP 49 path:
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
			return self.generate_ykeypath(path_indices)
		except ValueError as err:
			print(f'Error occurred: {err}.')

	def gen_bip84_path(self, path):
		#FIXME: define BIP 84 (bech32/native segwit addresses)
		''' Derive a BIP 84 path:
				m/84'/coin_type'/account'/change/address_index
		'''
		path_indices = self.decode_path(path)
		try:
			if len(path_indices) < 5:
				raise ValueError('BIP 44 path `{path_indices}` is not valid')
			if path_indices[1] != 0x8000002C:
				raise ValueError('BIP 44 purpose `{path_indices[1]}` is not valid')
			if not self.is_hardened(path_indices[2]):
				raise ValueError('BIP 44 coin_type `{path_indices[2]}` is not valid')
			if not self.is_hardened(path_indices[3]):
				raise ValueError('BIP 44 account number `{path_indices[3]}` is not valid')
			return self.generate_keypath(path_indices)
		except ValueError as err:
			print(f'Error occurred: {err}.')
	
	def gen_segwit_addr(self, ypub):
		witness = b'\x00\x14' + self.hash160(ypub)
		enc = b58encode_check(b'\x05' + self.hash160(witness))
		print(enc)
		return enc
	
	def gen_yaddr_range(self, path, rnge):
		# generate the BIP 44 path down to the 4th level
		keypairs = self.gen_bip49_path(path)
		keys = keypairs[-1]
		# extract keys
		m_yprv, m_ypub = keys["prv"], keys["pub"]
		depth = int(5).to_bytes(1, endianness)
		addrs = []
		for i in range(rnge):
			yprv, ypub = self.gen_child_ykeys(m_yprv, m_ypub, depth, i)
			addrs.append(self.gen_segwit_addr(self.extract_pub(ypub)))
		return addrs


class BIP44(BIP32_Account):

	def __init__(self, ):
		pass
	

if __name__ == "__main__":
	rootseed = "67f93560761e20617de26e0cb84f7234aaf373ed2e66295c3d7397e6d7ebe882ea396d5d293808b0defd7edd2babd4c091ad942e6a9351e6d075a29d4df872af"
	# Generate the first address
	path = "m/49'/0'/0'/0"
	#generate_address_range(rootseed, path, 5)
	wallet = BIP32_Account(rootseed)
	b = BIP44()
	print(b)
	#addrs = wallet.gen_addr_range(path, 20)
	#print(addrs)
	addresses = wallet.gen_yaddr_range(path, 20)
	for addr in addresses:
		print(addr)
