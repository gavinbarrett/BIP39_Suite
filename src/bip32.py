import hmac
from base58 import b58encode_check
from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac, sha256, sha512
from bip39 import bip39, generate_rootseed
from secp256k1 import secp256k1, CurvePoint

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
	prvkey, chaincode = split_rootkey(key)
	return prvkey, chaincode

def compress_pubkey(pubkey):
	# encode the y coordinte in the first byte of the public key
	if pubkey.y & 1:
		return unhexlify('03' + hex(pubkey.x)[2:])
	return unhexlify('02' + hex(pubkey.x)[2:])

def generate_extended_pubkey(prvkey, chaincode):
	''' Generate the public key by multiplying the private key by the secp256k1 base point '''
	pubkey = secp256k1().generate_pubkey(int(prvkey.hex(), 16))
	# compress the public key's y coordinate
	pubkey = compress_pubkey(pubkey)
	# generate and return an xpub key encoded with base58check
	xpub = pubkey_v + b'\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + chaincode + pubkey
	return b58encode_check(xpub)

def generate_extended_prvkey(prvkey, chaincode):
	''' Generate the private key from a BIP39 seed '''
	xprv = prvkey_v + b'\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + chaincode + b'\x00' + prvkey
	return b58encode_check(xprv)


if __name__ == "__main__":
	xprv, xpub = generate_extended_keypair(unhexlify('fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542'))
	print(f'{xprv}\n{xpub}')
