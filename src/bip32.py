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
	return hmac.new(b'Bitcoin seed', seed, sha512).hexdigest()

def split_rootkey(rootkey):
	# split the root key into a master secret key and a master chain code
	length = len(rootkey)//2
	master_key, chain_code = rootkey[:length], rootkey[length:]
	if (int(master_key, 16) == 0) or (int(master_key, 16) > secp256k1().n):
		raise ValueError("Master key is not valid!")
	return unhexlify(master_key), unhexlify(chain_code)

def generate_extended_keypair(rootseed):
	# generate a private secret from the rootseed
	prv, chaincode = generate_secret(rootseed)
	# generate the extended key pair
	return generate_extended_prvkey(prv, chaincode), generate_extended_pubkey(prv, chaincode)

def generate_secret(rootseed):
	# generate the master node
	key = generate_rootkey(rootseed)
	# split the private key from the chain code
	return split_rootkey(key)

def int2bytes(n):
	if n.bit_length() % 8 == 0:
		return n.bit_length() // 8
	return (n.bit_length() + (8 - (n.bit_length() % 8))) // 8

def compress_pubkey(pubkey):
	# encode the y coordinte in the first byte of the public key
	if pubkey.y & 1:
		return unhexlify('03' + hex(pubkey.x)[2:])
	return unhexlify('02' + hex(pubkey.x)[2:])

def extract_prv(prv):
	''' Extracts a private key from a '''
	decoded = b58decode_check(prv.encode())
	return decoded[-64:], decoded[26:90]

def hmac_parentkey(prv, chain):
	''' Ratchets the child key from the parent private key and chain code'''
	if int(prv.hex(), 16) >= 0x80000000:
		return hmac.new(chain, b'\x00' + prv.hex().encode() + b'\x00', sha512).hexdigest()
	return hmac.new(chain, prv.hex().encode() + b'\x00', sha512).hexdigest()

def split_childkey(childkey):
	''' Split the childkey in half '''
	length = len(childkey)//2
	return childkey[:length], childkey[length:]

def generate_child_prvkey(prv):
	ex_prv, chain = extract_prv(prv)
	#print(f'ex_prv: {ex_prv}\nchain: {chain}')
	child = hmac_parentkey(ex_prv, chain)
	child_prv, child_chain = split_childkey(child)
	fingerprint = generate_fingerprint(prv)
	'''
	print(f'child_prv: {child_prv}')
	print(f'ex_prv: {ex_prv}')
	print(f'secp256k1().n: {secp256k1().n}')
	print(f'child_chain: {child_chain}')
	'''
	child_prv = int(child_prv, 16) + int(ex_prv.hex(), 16) % secp256k1().n
	#FIXME: check if derived key is valid
	
	# child_prv.to_bytes(int2bytes(child_prv), sys.byteorder)
	newkey = prvkey_v + b'\x01' + fingerprint + b'\x00\x00\x00\x00' + unhexlify(child_chain) +  b'\x00' + child_prv.to_bytes(int2bytes(child_prv), byteorder)
	return b58encode_check(newkey)

def generate_fingerprint(xkey):
	# hash the parent key with sha256
	sha = sha256()
	sha.update(xkey.encode())
	# hash the digest with ripemd160
	ripemd = hashlib.new('ripemd160')
	ripemd.update(sha.digest())
	# return the first four bytes of the checksum
	return ripemd.digest()[:4]

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
	return b58encode_check(xpub).decode()

def generate_extended_prvkey(prvkey, chaincode):
	''' Generate the private key from a BIP39 seed '''
	xprv = prvkey_v + b'\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + chaincode + b'\x00' + prvkey
	return b58encode_check(xprv).decode()


if __name__ == "__main__":
	xprv, xpub = generate_extended_keypair(unhexlify('000102030405060708090a0b0c0d0e0f'))
	#print(f'{xprv}\n{xpub}')
	c = generate_child_prvkey(xprv)
	print(c)
