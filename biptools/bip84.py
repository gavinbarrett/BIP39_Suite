import sys
import struct
from binascii import unhexlify
from base58 import b58encode_check
from biptools.bip32 import BIP32_Account
from biptools.secp256k1 import secp256k1, CurvePoint

def bech32_polymod(values):
  GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
  chk = 1
  for v in values:
    b = (chk >> 25)
    chk = (chk & 0x1ffffff) << 5 ^ v
    for i in range(5):
      chk ^= GEN[i] if ((b >> i) & 1) else 0
  return chk

def bech32_hrp_expand(s):
  return [ord(x) >> 5 for x in s] + [0] + [ord(x) & 31 for x in s]

def bech32_verify_checksum(hrp, data):
  return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1

def bech32_create_checksum(hrp, data):
	values = bech32_hrp_expand(hrp) + data
	polymod = bech32_polymod(values + [0,0,0,0,0,0]) ^ 1
	return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

class BIP84(BIP32_Account):
	def __init__(self, seed, fromseed=False, salt=""):
		super().__init__(seed, fromseed, salt)
		self.prv_version = b'\x04\xb2\x43\x0c'
		self.pub_version = b'\x04\xb2\x47\x46'
		self.master_prv, self.master_pub = self.derive_master_keys()
		self.alphabet = list('qpzry9x8gf2tvdw0s3jn54khce6mua7l')

	def derive_master_keys(self):
		''' Generate a master extended key pair '''
		depth = b'\x00'
		m_id = b'\x00' * 4
		return self.gen_prv(depth, m_id, m_id, self.master_prv, self.master_chain), self.gen_pub(depth, m_id, m_id, self.master_prv, self.master_chain)

	def get_master_keys(self):
		''' Return the master xkeys '''
		return self.master_prv, self.master_pub

	def gen_prv(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the private key from a BIP39 seed '''
		zprv = self.prv_version + depth + fingerprint + index + chaincode + b'\x00' + prvkey
		return b58encode_check(zprv).decode()

	def gen_pub(self, depth, fingerprint, index, prvkey, chaincode):
		''' Generate the public key by multiplying the private key by the secp256k1 base point '''
		pubkey = self.point(prvkey)
		try:
			# compress the public key's y coordinate
			pubkey = self.compress_pubkey(pubkey)
		except ValueError as v:
			print(f'Error: {v}')
		# generate and return an xpub key encoded with base58check
		zpub = self.pub_version + depth + fingerprint + index + chaincode + pubkey
		return b58encode_check(zpub).decode()

	def gen_child_zkeys(self, zprv, zpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.generate_child_prvkey(zprv, zpub, depth, index, self.prv_version)
		# generate child extended public key
		child_pub = self.generate_child_pubkey(child_prv, zpub, depth, index, self.pub_version)
		return child_prv, child_pub

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
	
	def derive_child_keys(self, zprv, zpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.derive_child_prvkey(zprv, zpub, depth, index)
		# generate child extended public key
		child_pub = self.derive_child_pubkey(child_prv, zpub, depth, index)
		return child_prv, child_pub
	
	def derive_child_prvkey(self, zprv, zpub, depth, index):
		# extract private, public, and chain code
		prv, chain = self.extract_prv(zprv)
		pub = self.extract_pub(zpub)
		# generate the private child key
		child = self.ckd_prv(prv, chain, index)
		# split the private key and chain code
		child_prv, child_chain = self.split_childkey(child)
		# generate the fingerprint for the key
		fingerprint = self.generate_fingerprint(pub)
		# generate child private key
		child_prv = (int(child_prv, 16) + int(prv.hex(), 16)) % secp256k1().n
		#FIXME: check if derived key is valid
		child_zprv = self.prv_version + depth + fingerprint + index + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(32, self.endianness)
		return b58encode_check(child_zprv).decode()

	def derive_child_pubkey(self, child_prv, parent_pub, depth, index):
		''' Generate a child public key '''
		# extract child private key and chain code
		child_prv, child_chain = self.extract_prv(child_prv)
		# generate and compress child public key
		child_pub = self.compress_pubkey(self.point(child_prv))
		# generate the parent fingerprint from the public key
		fingerprint = self.generate_fingerprint(self.extract_pub(parent_pub))
		# serialize the child xpub key
		child_zpub = self.pub_version + depth + fingerprint + index + child_chain + child_pub
		# return the child xpub key encoded in bas58_check
		return b58encode_check(child_zpub).decode()
	
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
				zprv, zpub = self.get_master_keys()
			else:
				try:
					# ensure that key index and depth variables do not overflow
					if not (0x00 <= depth <= 0xff):
						raise ValueError(f'Invalid key depth {depth}')
					if not (0x00 <= index <= 0xffffffff):
						raise ValueError(f'Invalid key index {index}')
					# Generate a child extended key pair
					zprv, zpub = self.derive_child_keys(zprv, zpub, depth.to_bytes(1, self.endianness), index)
				except ValueError as err:
					print(f'Error deriving child key: {err}.')
					return None
			keypairs.append({"prv": zprv, "pub": zpub})
		return keypairs
	
	def encode_bits(self, bytestring):
		# reverse byte so that most significant bit of each byte is first
		bstring = int.from_bytes(bytestring, 'big')
		# encode the bytes into the character set
		return [(bstring >> i) & 0x1f for i in range(0, 160, 5)][::-1]

	def bech_encode(self, witness):
		# set the human readable portion
		hrp = 'bc'
		# append the bech32 checksum
		witness = [0] + self.encode_bits(witness)
		# append checksum 
		witness = witness + bech32_create_checksum(hrp, witness)
		# serialize the address
		return hrp + '1' + ''.join([self.alphabet[idx] for idx in witness])

	def derive_address(self, pub):
		''' Generate a legacy Bitcoin address '''
		# hash the public key with sha256 and then ripemd160; prepend it with 0x00
		pubkey_hash = b'\x00' + self.hash160(pub)
		# encode the hash
		return self.bech_encode(pubkey_hash)

	def gen_addr_range(self, path, rnge, hardened=False):
		# generate the BIP 44 path down to the 4th level
		keypairs = self.derive_path(path)
		keys = keypairs[-1]
		# extract keys
		m_zprv, m_zpub = keys["prv"], keys["pub"]
		depth = int(5).to_bytes(1, self.endianness)
		addresses = []
		offset = 2**31 if hardened else 0
		for i in range(rnge):
			# derive the extended key pair for i'
			zprv, zpub = self.derive_child_keys(m_zprv, m_zpub, depth, i + offset)
			# add the associated address
			addresses.append(self.derive_address(self.extract_pub(zpub)))
		return addresses
