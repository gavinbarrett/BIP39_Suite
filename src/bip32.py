import hmac
import hashlib
import struct
from sys import byteorder
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
	def __init__(self, mnemonic, salt):
		# Generate BIP 39 root seed
		self.rootseed = generate_rootseed(mnemonic, salt)
		# Generate master extended private and public keys
		#FIXME: self.master_xprv, self.master_xpub = generate_extended_keypair(self.rootseed)
	def printXPUB(self):
		print(self.master_xpub)

def generate_rootkey(seed):
	# derive the root key from the BIP39 seed
	return hmac.digest(b'Bitcoin seed', seed, sha512).hex()

def split_rootkey(rootkey):
	# split the root key into a master secret key and a master chain code
	length = len(rootkey) // 2
	master_key, chain_code = rootkey[:length], rootkey[length:]
	if (int(master_key, 16) <= 0) or (int(master_key, 16) >= secp256k1().n):
		raise ValueError("Master key is not valid!")
	return unhexlify(master_key), unhexlify(chain_code)

def generate_secret(rootseed):
	# generate the master node
	key = generate_rootkey(rootseed)
	# split the private key from the chain code
	return split_rootkey(key)

def amt_bytes(n):
	''' Convert an arbitrary integer into a stream of bytes '''
	if n.bit_length() % 8 == 0:
		return n.bit_length() // 8
	return (n.bit_length() + (8 - (n.bit_length() % 8))) // 8

def point(prv_key):
	# compute the public key: K = k*G
	return secp256k1().generate_pubkey(int.from_bytes(prv_key, endianness))

def compress_pubkey(pubkey):
	# encode the y coordinte in the first byte of the public key
	if pubkey.y & 1:
		return unhexlify('03' + hex(pubkey.x)[2:])
	return unhexlify('02' + hex(pubkey.x)[2:])

def extract_prv(prv):
	''' Extracts a private key and the chain code from an extended private key '''
	decoded = b58decode_check(prv.encode())
	return decoded[-32:], decoded[13:45]

def extract_pub(pub):
	''' Extracts a public key from an extended public key '''
	decoded = b58decode_check(pub.encode())
	return decoded[-33:]

def split_childkey(childkey):
	''' Split the childkey in half '''
	length = len(childkey) // 2
	return childkey[:length], childkey[length:]

def hash160(pubkey):
	# hash the parent key with sha256
	sha = sha256()
	sha.update(pubkey)
	# hash the digest with ripemd160
	ripemd = hashlib.new('ripemd160')
	ripemd.update(sha.digest())
	return ripemd.digest()

def generate_fingerprint(pubkey):
	''' Return the first four bytes of the hash160 '''
	return hash160(pubkey)[:4]

def hmac_key(chain, data):
	# hash a key appended with the index with hmac keyed with the chain code and using sha512
	return hmac.new(chain, data, sha512).hexdigest()

def generate_child_keypair():
	pass

def ckd_prv(prv, chain, index):
	''' Derives the child key from the parent private key and chain code
		CKDpriv:
		((k_par, c_par), i) -> (k_i, c_i)
	'''
	if int.from_bytes(index, endianness) >= 0x80000000:
		# child is a hardened key
		key = b'\x00' + prv + index
	else:
		# child is a normal key
		key = point(prv) + index
	# return the child private key
	return hmac_key(chain, key)

def generate_child_prvkey(xprv, xpub, index):
	# extract private, public, and chain code
	prv, chain = extract_prv(xprv)
	pub = extract_pub(xpub)
	# generate the private child key
	child = ckd_prv(prv, chain, index)
	# split the private key and chain code
	child_prv, child_chain = split_childkey(child)
	# generate the fingerprint for the key
	fingerprint = generate_fingerprint(pub)
	# generate child private key
	child_prv = (int(child_prv, 16) + int(prv.hex(), 16)) % secp256k1().n
	#FIXME: check if derived key is valid
	child_xprv = prvkey_v + b'\x01' + fingerprint + index + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(32, endianness)
	return b58encode_check(child_xprv).decode()

def generate_child_pubkey(child_prv, parent_pub, index):
	''' Generate a child public key '''
	# extract child private key and chain code
	child_prv, child_chain = extract_prv(child_prv)
	# generate and compress child public key
	child_pub = compress_pubkey(point(child_prv))
	# generate the parent fingerprint from the public key
	fingerprint = generate_fingerprint(extract_pub(parent_pub))
	# serialize the child xpub key
	child_xpub = pubkey_v + b'\x01' + fingerprint + index + child_chain + child_pub
	# return the child xpub key encoded in bas58_check
	return b58encode_check(child_xpub).decode()

def generate_master_extended_keypair(rootseed):
	''' Generate a master extended key pair '''
	depth = b'\x00'
	# set master key index (0x00) and master key fingerprint (0x00000000)
	master_id = b'\x00' * 4
	# generate a private secret from the rootseed
	prv_key, chain_code = generate_secret(rootseed)
	# generate the extended key pair
	return generate_extended_prvkey(depth, master_id, master_id, prv_key, chain_code), generate_extended_pubkey(depth, master_id, master_id, prv_key, chain_code)

def generate_extended_prvkey(depth, fingerprint, index, prvkey, chaincode):
	''' Generate the private key from a BIP39 seed '''
	xprv = prvkey_v + depth + fingerprint + index + chaincode + b'\x00' + prvkey
	return b58encode_check(xprv).decode()

def generate_extended_pubkey(depth, fingerprint, index, prvkey, chaincode):
	''' Generate the public key by multiplying the private key by the secp256k1 base point '''
	pubkey = point(prvkey)
	try:
		# compress the public key's y coordinate
		pubkey = compress_pubkey(pubkey)
	except ValueError as v:
		print(f'Error: {v}')
	# generate and return an xpub key encoded with base58check
	xpub = pubkey_v + depth + fingerprint + index + chaincode + pubkey
	return b58encode_check(xpub).decode()


if __name__ == "__main__":
	xprv, xpub = generate_master_extended_keypair(unhexlify('000102030405060708090a0b0c0d0e0f'))
	print(f'{xprv}\n{xpub}\n')
	child_index = struct.pack('>L', 2**31)
	child_xprv = generate_child_prvkey(xprv, xpub, child_index)
	child_xpub = generate_child_pubkey(child_xprv, xpub, child_index)
	print(f'{child_xprv}\n{child_xpub}')
