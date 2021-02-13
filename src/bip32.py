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

# public key version metadata
pubkey_v = b'\x04\x88\xB2\x1E'
# private key version metadata
prvkey_v = b'\x04\x88\xAD\xE4'
# set byte endianness
endianness = 'big'

class BIP32_Account:
	def __init__(self, rootseed):
		# Generate BIP 39 root seed
		self.rootseed = rootseed#generate_rootseed(mnemonic, salt)
		# Generate master extended private and public keys
		#FIXME: self.master_xprv, self.master_xpub = generate_extended_keypair(self.rootseed)
		#self.rootkey = self.generate_rootkey(self.rootseed)

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

	def generate_legacy_address(self, xpub):
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

	def generate_child_prvkey(self, xprv, xpub, depth, index):
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
		child_xprv = prvkey_v + depth + fingerprint + index + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(32, endianness)
		return b58encode_check(child_xprv).decode()

	def generate_child_pubkey(self, child_prv, parent_pub, depth, index):
		''' Generate a child public key '''
		# extract child private key and chain code
		child_prv, child_chain = self.extract_prv(child_prv)
		# generate and compress child public key
		child_pub = self.compress_pubkey(self.point(child_prv))
		# generate the parent fingerprint from the public key
		fingerprint = self.generate_fingerprint(self.extract_pub(parent_pub))
		# serialize the child xpub key
		child_xpub = pubkey_v + depth + fingerprint + index + child_chain + child_pub
		# return the child xpub key encoded in bas58_check
		return b58encode_check(child_xpub).decode()

	def generate_master_extended_keypair(self, rootseed):
		''' Generate a master extended key pair '''
		depth = b'\x00'
		# set master key index (0x00) and master key fingerprint (0x00000000)
		master_id = b'\x00' * 4
		# generate a private secret from the rootseed
		prv_key, chain_code = self.generate_secret(rootseed)
		# generate the extended key pair
		return self.generate_extended_prvkey(depth, master_id, master_id, prv_key, chain_code), self.generate_extended_pubkey(depth, master_id, master_id, prv_key, chain_code)

	def generate_extended_prvkey(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the private key from a BIP39 seed '''
		xprv = prvkey_v + depth + fingerprint + index + chaincode + b'\x00' + prvkey
		return b58encode_check(xprv).decode()

	def generate_extended_pubkey(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the public key by multiplying the private key by the secp256k1 base point '''
		pubkey = self.point(prvkey)
		try:
			# compress the public key's y coordinate
			pubkey = self.compress_pubkey(pubkey)
		except ValueError as v:
			print(f'Error: {v}')
		# generate and return an xpub key encoded with base58check
		xpub = pubkey_v + depth + fingerprint + index + chaincode + pubkey
		return b58encode_check(xpub).decode()

	def generate_child_keypair(self, xprv, xpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.generate_child_prvkey(xprv, xpub, depth, index)
		# generate child extended public key
		child_pub = self.generate_child_pubkey(child_prv, xpub, depth, index)
		return child_prv, child_pub

	def generate_keypath(self, rootkey, path_indices):
		''' Generate a BIP wallet chain along a given path '''
		# decode the chain's path
		keypairs = []
		for depth, index in enumerate(path_indices):
			if index == "m":
				# Generate the master extended key pair
				xprv, xpub = self.generate_master_extended_keypair(unhexlify(rootkey))
			else:
				try:
					# ensure that key index and depth variables do not overflow
					if not (0x00 <= depth <= 0xff):
						raise ValueError(f'Invalid key depth {depth}')
					if not (0x00 <= index <= 0xffffffff):
						raise ValueError(f'Invalid key index {index}')
					# Generate a child extended key pair
					xprv, xpub = self.generate_child_keypair(xprv, xpub, depth.to_bytes(1, endianness), index)
				except ValueError as err:
					print(f'Error deriving child key: {err}.')
					return None
			keypairs.append({"prv": xprv, "pub": xpub})
		return keypairs


	def generate_address_range(self, rootkey, path, rnge):
		# generate the BIP 44 path down to the 4th level
		keypairs = self.generate_bip44_path(rootkey, path)
		keys = keypairs[-1]
		# extract keys
		m_xprv, m_xpub = keys["prv"], keys["pub"]
		depth = int(5).to_bytes(1, endianness)
		for i in range(rnge):
			xprv, xpub = self.generate_child_keypair(m_xprv, m_xpub, depth, i)
			print(f'add: {self.generate_legacy_address(self.extract_pub(xpub))}')
			print(f'pub: {self.extract_pub(xpub).hex()}')
			print(f'prv: {self.wif_encode_prv(xprv)}\n')


	def generate_bip44_path(self, rootkey, path):
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
			return self.generate_keypath(rootkey, path_indices)
		except ValueError as err:
			print(f'Error occurred: {err}.')


if __name__ == "__main__":
	rootseed = "1b7a95e4ee67157b6d369add2dddd2152a5182ba112f882395ec6648efe36fb7a60bb6c4587210fdaca4cef2aa1de06c20f2468eca196beb34bf73fbe652d88f"
	# Generate the first address
	path = "m/44'/0'/0'/0"
	#generate_address_range(rootseed, path, 5)
	wallet = BIP32_Account(rootseed)
	wallet.generate_address_range(wallet.rootseed, path, 5)
