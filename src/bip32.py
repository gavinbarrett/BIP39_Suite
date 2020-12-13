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

def generate_extended_privkey(mnemonic_phrase):
	''' Generate an extended private key (k, c) consisting of a main key (k) and a chain code (c) '''
	version = b'\x04\x88\xAD\xE4'
	depth = b'\x00'
	fingerprint = b'\x00\x00\x00\x00'
	child_num = b'\x00\x00\x00\x00'
	# generate the rootseed with PBKDF2_HMAC and passphrase `mnemonic`
	seed = generate_rootseed(mnemonic_phrase, '')
	return seed

def generate_extended_privkey2(rootseed):
	''' Generate an xpriv key from a BIP39 seed '''
	print(f'BIP39 Root Seed: {rootseed}\n')
	key = generate_rootkey(rootseed)
	print(f'BIP32 Master Node: {key}\n')
	try:
		secret_key, chain_code = split_rootkey(key)
		version = b'\x04\x88\xAD\xE4'
		depth = b'\x00'
		fingerprint = b'\x00\x00\x00\x00'
		child_num = b'\x00\x00\x00\x00'

		print(f'Master key: {hexlify(secret_key)}')
		print(f'Chain code: {hexlify(chain_code)}\n')
		
		priv = version + depth + fingerprint + child_num + chain_code + b'\x00' + secret_key
		
		print(f'{hexlify(priv)} {hexlify(checksum)}\n')
		print(f'Computed key: {b58encode_check(priv)}')
	
		print(f'Expected xpriv: 0488ade400000000000000000044aed744c1c30eb0298c1586eac257de5f27af381a6842059360dfd89c8055af00582badc354dcfff186212d43aa1b02cfe1a51c37e012a78bd77b2f6bdee3bebe eda25f5a')

	except ValueError as ve:
		print(f'Error: {ve}')


if __name__ == "__main__":

	generate_extended_privkey2(unhexlify('a83930217f6671af4a1a1bcef98f41c52d0ea70bed8d92b7fbdb8d531efa6d312fe2e2a15acf743387072bdace60cba2846449527f1f8f793fc6abd7d854ae8d'))
