import hmac
import hashlib
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

def int2bytes(n):
	''' Convert an arbitrary integer into a stream of bytes '''
	if n.bit_length() % 8 == 0:
		return n.bit_length() // 8
	return (n.bit_length() + (8 - (n.bit_length() % 8))) // 8

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

def hmac_key(chain, data):
	return hmac.new(chain, data, sha512).hexdigest()

def hmac_parentkey(prv, pub, chain, i):
	''' Derives the child key from the parent private key and chain code
		CKDpriv:
		((k_par, c_par), i) -> (k_i, c_i)
	'''
	# FIXME: Not computing the correct child key from parent key
	print(f'\nPRV: {prv.hex()}')
	print(f'PUB: {pub.hex()}')
	print(f'CHA: {chain.hex()}')
	index = int(i).to_bytes(4, 'big')
	if int(prv.hex(), 16) >= 0x80000000:
		# child is a hardened key
		key = b'\x00' + prv + index
	else:
		# child is a normal key
		key = pub + index
	# return the child private key
	return hmac_key(chain, key)

def generate_child_prvkey(xprv, xpub):
	# extract private, public, and chain code
	i = 0x80000000
	prv, chain = extract_prv(xprv)
	pub = extract_pub(xpub)
	# generate the private child key
	child = hmac_parentkey(prv, pub, chain, i)
	# split the private key and chain code
	child_prv, child_chain = split_childkey(child)
	# generate the fingerprint for the key
	fingerprint = generate_fingerprint(pub)
	print(f'child_prv: {child_prv}')
	child_prv = (int(child_prv, 16) + int(prv.hex(), 16)) % secp256k1().n
	#FIXME: check if derived key is valid
	
	#print(f'\nFNG: {fingerprint.hex()}')
	#print(f'new prv:   {hex(child_prv)[2:]}')
	#print(f'new chain: {child_chain}\n')
	
	# child_prv.to_bytes(int2bytes(child_prv), sys.byteorder)
	newkey = prvkey_v + b'\x01' + fingerprint + i.to_bytes(4, 'big') + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(int2bytes(child_prv), 'big')
	print(f'fingerprint: {fingerprint}')
	print(f'child_chain: {child_chain}')
	print(f'child_prv: {hex(child_prv)[2:]}')
	print(f'Newkey: {newkey.hex()}')
	print(f'Oldkey: 0488ade4013442193e8000000047fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae623614100edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea')
	old_key = '0488ade4013442193e8000000047fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae623614100edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea'
	assert(newkey.hex() == old_key)
	return b58encode_check(newkey).decode()

def hash160(pubkey):
	# hash the parent key with sha256
	sha = sha256()
	sha.update(pubkey)
	# hash the digest with ripemd160
	ripemd = hashlib.new('ripemd160')
	ripemd.update(sha.digest())
	return ripemd.digest()

def generate_fingerprint(pubkey):
	# return the first four bytes of the hash160
	#print(f'BBB: {pubkey}')
	return hash160(pubkey)[:4]

def generate_extended_keypair(rootseed):
	# generate a private secret from the rootseed
	prv, chaincode = generate_secret(rootseed)
	# generate the extended key pair
	return generate_extended_prvkey(prv, chaincode), generate_extended_pubkey(prv, chaincode)

def point(prv):
	chain = '873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508'
	pubkey = secp256k1().generate_pubkey(int(prv, 16))
	#print(pubkey)
	key = hex(pubkey.y)[2:] + hex(pubkey.x)[2:]
	print(key)
	h = hmac.digest(unhexlify(chain), unhexlify(key) + b'\x00\x00\x00\x00', sha512).hex()
	l = len(h) // 2
	print(h[:l])
	print(h[l:])

def generate_extended_pubkey(prvkey, chaincode):
	''' Generate the public key by multiplying the private key by the secp256k1 base point '''
	pubkey = secp256k1().generate_pubkey(int(prvkey.hex(), 16))
	try:
		# compress the public key's y coordinate
		pubkey = compress_pubkey(pubkey)
	except ValueError as v:
		print(f'Error: {v}')
	# generate and return an xpub key encoded with base58check
	xpub = pubkey_v + b'\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + chaincode + pubkey
	#ser_xpub = '0488b21e000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d5080339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2'
	#assert(xpub.hex() == ser_xpub)
	return b58encode_check(xpub).decode()

def generate_extended_prvkey(prvkey, chaincode):
	''' Generate the private key from a BIP39 seed '''
	xprv = prvkey_v + b'\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + chaincode + b'\x00' + prvkey
	#ser_xprv = '0488ade4000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d50800e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35'
	#assert(xprv.hex() == ser_xprv)
	return b58encode_check(xprv).decode()


if __name__ == "__main__":
	xprv, xpub = generate_extended_keypair(unhexlify('000102030405060708090a0b0c0d0e0f'))
	print(f'{xprv}\n{xpub}')
	c = generate_child_prvkey(xprv, xpub)
	print(c)
