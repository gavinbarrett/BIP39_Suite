import hmac
from base58 import b58encode_check
from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac, sha256, sha512
from bip39 import bip39, generate_rootseed
from secp256k1 import secp256k1

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

def generate_extended_privkey(rootseed):
	''' Generate an xpriv key from a BIP39 seed '''
	key = generate_rootkey(rootseed)
	try:
		secret_key, chain_code = split_rootkey(key)
		version = b'\x04\x88\xAD\xE4'
		depth = b'\x00'
		fingerprint = b'\x00\x00\x00\x00'
		child_num = b'\x00\x00\x00\x00'

		print(f'Master key: {hexlify(secret_key)}')
		#print(f'Chain code: {hexlify(chain_code)}\n')
		
		xprv = version + depth + fingerprint + child_num + chain_code + b'\x00' + secret_key
		
		print(len(secret_key))
		return b58encode_check(xprv)
	except ValueError as ve:
		print(f'Error: {ve}')


if __name__ == "__main__":
	print(generate_extended_privkey(unhexlify('fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542')))
