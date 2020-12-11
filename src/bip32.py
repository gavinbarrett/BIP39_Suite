from hashlib import pbkdf2_hmac
from binascii import hexlify, unhexlify
from bip39 import bip39, generate_rootseed

public_version = 0x0488B21E
private_version = 0x0488ADE4

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
	return rootkey[:len(rootkey)//2], rootkey[len(rootkey)//2:]

def generate_child_privkey():
	pass

def generate_child_pubkey():
	pass

def serialize_extended_key():
	pass



if __name__ == "__main__":
	seed = generate_rootseed('code glare comic flip burden toward apology fiction grain feel supply blossom', '')
	print(seed)

