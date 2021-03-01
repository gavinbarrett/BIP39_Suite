import json
import hmac
import hashlib
import struct
from sys import byteorder, exit
from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac, sha256, sha512
from biptools.bip39 import BIP39
from biptools.secp256k1 import secp256k1, CurvePoint
from base58 import b58encode, b58encode_check, b58decode, b58decode_check

class BIP32_Account:
	# FIXME: 	ideally we should be passing in a custom class to prevent people from using this construtor to
	#			creating brain wallets
	def __init__(self, seed, fromseed=False, salt=''):
		# Generate BIP 32 master keys
		if fromseed:
			# constructing from BIP39 seed
			self.rootseed = unhexlify(seed)
		else:
			# constructing from an ascii BIP39 mnemonic phrase
			self.rootseed = BIP39().generate_rootseed(seed, salt)
		self.rootnode = self.generate_rootkey(self.rootseed)
		self.master_prv, self.master_chain = self.split_rootkey(self.rootnode)
		self.endianness = 'big'

	# FIXME: create valid_key/on_curve function
	def generate_rootkey(self, seed):
		# derive the root key from the BIP39 seed
		return hmac.digest(b'Bitcoin seed', seed, sha512).hex()
	
	def hmac_key(self, chain, data):
		# hash a key appended with the index with hmac keyed with the chain code and using sha512
		return hmac.new(chain, data, sha512).hexdigest()
	
	def point(self, prv_key):
		# compute the public key: K = k*G
		private = int.from_bytes(prv_key, self.endianness)
		return secp256k1().generate_pubkey(private)
	
	def compress_pubkey(self, pubkey):
		# return the compressed public key
		if pubkey.y & 1:
			return b'\x03' + pubkey.x.to_bytes(32, self.endianness)
		return b'\x02' + pubkey.x.to_bytes(32, self.endianness)

	def extract_prv(self, prv):
		''' Extracts a private key and the chain code from an extended private key '''
		decoded = b58decode_check(prv.encode())
		return decoded[-32:], decoded[13:45]

	def extract_pub(self, pub):
		''' Extracts a public key from an extended public key '''
		decoded = b58decode_check(pub.encode())
		return decoded[-33:]

	def split_rootkey(self, rootkey):
		# split the root key into a master secret key and a master chain code
		length = len(rootkey) // 2
		master_key, chain_code = rootkey[:length], rootkey[length:]
		if (int(master_key, 16) <= 0) or (int(master_key, 16) >= secp256k1().n):
			raise ValueError("Master key is not valid!")
		return unhexlify(master_key), unhexlify(chain_code)
	
	def split_childkey(self, childkey):
		''' Split the childkey in half '''
		length = len(childkey) // 2
		return childkey[:length], childkey[length:]

	def wif_encode_prv(self, xprv):
		''' Encrypt a private key in WIF format '''
		# extract private key
		prv, chain = self.extract_prv(xprv)
		# encode private key with WIF codes
		return b58encode_check(b'\x80' + prv + b'\x01')

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

	def generate_fingerprint(self, pubkey):
		''' Return the first four bytes of the hash160 '''
		return self.hash160(pubkey)[:4]

	def is_hardened(self, index):
		''' Return true if a number falls within range of a hardened key index '''
		return 2**31 <= index <= 2**32

	def ckd_prv(self, prv, chain, index):
		''' Derives the child key from the parent private key and chain code
			CKDpriv:
			((k_par, c_par), i) -> (k_i, c_i)
		'''
		if int.from_bytes(index, self.endianness) >= 0x80000000:
			# child is a hardened key
			key = b'\x00' + prv + index
		else:
			# child is a normal key
			key = self.compress_pubkey(self.point(prv)) + index
		# return the child private key
		return self.hmac_key(chain, key)

	def derive_child_prvkey(self, xprv, xpub, depth, index):
		pass

	def derive_child_pubkey(self, child_prv, parent_pub, depth, index):
		pass
