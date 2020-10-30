from sys import exit
from seeds import *
from entropy import *
from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac

def bip39(entropy, size):
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
	#print(f'1. Entropy: {binent}')
	
	# extract the checksum from the digest
	check = checksum(digest, length, size * 8)
	#print(f'2. Checksum: {check}')

	# append checksum to the entropy
	concat = concat_checksum(binent, check);
	#print(f'Concat: {concat}\n')

	# split buffer into groups of 11
	splits = split_entropy(concat, size)

	# extract words from mnemonic word file
	words = gather_words()

	exp = "ozone drill grab fiber curtain grace pudding thank cruise elder eight picnic"
	exps = exp.split(' ')
	idxs = [bin(words.index(e))[2:] for e in exps]
	#print(' '.join(idxs))
	#print('\n')
	#bins = [words[s] for s in splits]

	#print(' '.join(splits))

	seeds = [words[int(s, 2)] for s in splits]
	
	seedphrase = ' '.join(seeds)

	#print(seedphrase, end='\n\n')

	return seedphrase
