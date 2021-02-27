from src.seeds import *
from src.entropy import *
from sys import exit
from hashlib import pbkdf2_hmac
from binascii import hexlify

# map desired mnemonic phrase length with bytes of entropy
mnemonic_bytemap = {'12': 16, '15': 20, '18': 24, '21': 28, '24': 32}

def generate_entropy(size, entropy):
	# generate entropy
	if not entropy:
		try:
			entropy = generate(size)
			return entropy
		except ValueError as error:
			print(f'ERROR: {error}')
			exit(0)
	# return injected test case entropy
	return entropy

def entropy_string(size, entropy):
	# return entropy bytes as a padded binary string
	return pad_string(bin(int.from_bytes(entropy, 'big'))[2:], size * 8)

def bip39(size, entropy=None):
	# generate entropy
	entropy = generate_entropy(size, entropy)
	# extract words from mnemonic word file
	words = gather_words()
	# generate the checksum length
	length = get_length(size)
	# generate the SHA-256 digest of the entropy
	digest = sha_hash(entropy)
	# turn entropy into a padded binary string 
	binary = entropy_string(size, entropy)
	# extract the checksum from the digest
	check = checksum(digest, length, size * 8)
	# append checksum to the entropy
	concat = binary + check
	# split buffer into groups of 11
	splits = split_entropy(size, concat)
	# interpret entropy strings as integers
	seeds = [words[int(s, 2)] for s in splits]
	return ' '.join(seeds)

def generate_rootseed(mnemonics, salt):
	# return the seed generated from the mnemonic phrase
	return pbkdf2_hmac('sha512', mnemonics.encode('utf-8'), ('mnemonic' + salt).encode('utf-8'), 2048, 64)
