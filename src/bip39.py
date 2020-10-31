from seeds import *
from entropy import *
from sys import exit
from hashlib import pbkdf2_hmac

def bip39(size, entropy=None):
	# generate entropy
	if not entropy:
		try:
			entropy = generate(size)
		except ValueError as error:
			print(f'ERROR: {error}')
			exit(0)

	# generate the checksum length
	length = get_length(size)

	# generate the SHA-256 digest of the entropy
	digest = sha_hash(entropy)

	binent = pad(bin(int.from_bytes(entropy, 'big'))[2:], size * 8)
	
	# extract the checksum from the digest
	check = checksum(digest, length, size * 8)

	# append checksum to the entropy
	concat = concat_checksum(binent, check);

	# split buffer into groups of 11
	splits = split_entropy(concat, size)

	# extract words from mnemonic word file
	words = gather_words()

	seeds = [words[int(s, 2)] for s in splits]
	
	return ' '.join(seeds)
