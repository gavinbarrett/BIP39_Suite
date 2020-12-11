from base58 import b58encode
from hashlib import pbkdf2_hmac, sha256
from binascii import hexlify, unhexlify
from bip39 import bip39, generate_rootseed

class secp256k1():
	# This class represents the secp256k1 elliptic curve: y^2 = x^3 + b (mod p)
	# Parameters sourced from https://en.bitcoin.it/wiki/Secp256k1
	def __init__(self):
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
		self.b = 0x0000000000000000000000000000000000000000000000000000000000000007
		self.x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
		self.y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
		self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def point_mult(p):
	# FIXME: perform EC point addition with secp256k1 parameters
	curve = secp256k1()
	K = 0
	for i in range(p):
		K += (curve.b) % curve.n

def generate_rootkey(seed):
	# derive the root key from the BIP39 seed
	return hexlify(pbkdf2_hmac('sha512', seed, b'Bitcoin seed', 2048, 64))

def split_rootkey(rootkey):
	# split the root key into a master secret key and a master chain code
	length = len(rootkey)//2
	master_key, chain_code = rootkey[:length], rootkey[length:]
	if (int(master_key, 16) == 0) or (int(master_key, 16) > secp256k1().n):
		raise ValueError("Master key is not valid!")
	return unhexlify(master_key), unhexlify(chain_code)

def generate_extended_privkey(mnemonic_phrase):
	''' Generate an extended private key (k, c) consisting of a main key (k) and a chain code (c) '''
	version = 0x0488ADE4
	depth = 0x00
	fingerprint = 0x00000000
	child_num = 0x00000000

	# generate the rootseed with PBKDF2_HMAC and passphrase `mnemonic`
	seed = generate_rootseed(mnemonic_phrase)
	# generate the rootkey with PBKDF2_HMAC and passphrase `Bitcoin seed`
	rootkey = generate_rootkey(seed)

	#FIXME: add try/catch
	master_key, chain_code = split_rootkey(rootkey)

	return version + depth + fingerprint + child_num

def generate_extended_pubkey():
	pass

def generate_key_checksum(extended_key_matter):
	''' Generate a checksum for an extended key '''
	sha = sha256()
	# hash the private key with sha256
	sha.update(extended_key_matter)
	print(f'hash1: {sha.digest()}')
	# hash the hash of the private key with sha256
	sha.update(sha.digest())
	print(f'hash: {sha.digest()}')
	# extract the first four bits of the double hash
	return bytes(list(sha.digest())[:4])

def encode_extended_key():
	''' Encode an extended public or private key into base58 '''
	pass

def serialize_extended_key():
	pass



def generate_child_privkey():
	pass

def generate_child_pubkey():
	pass




if __name__ == "__main__":
	key = generate_rootkey(unhexlify('63a8ae155065a17dd29ffa5d52d096671a25821c96dd28169c75b789cde12bab89024a449f193403565972a1f39f2bd0eeb48600568495740b250d5c7dd0ef66'))
	print(key)
	try:
		secret_key, chain_code = split_rootkey(key)
		
		version = b'\x04\x88\xAD\xE4'
		depth = b'\x00'
		fingerprint = b'\x00\x00\x00\x00'
		child_num = b'\x00\x00\x00\x00'
		
		priv = version + depth + fingerprint + child_num + chain_code + b'\x00' + secret_key
		
		checksum = generate_key_checksum(priv)

		priv = priv + checksum

		print(b58encode(priv))
	except ValueError as ve:
		print(f'Error: {ve}')
	
