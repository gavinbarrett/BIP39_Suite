from sys import exit
from seeds import *
from entropy import *
from binascii import hexlify
from hashlib import pbkdf2_hmac

def bip39(entropy, size):
	# generate entropy
	if not entropy:
		try:
			entropy = generate(size)
		except ValueError as error:
			print(f'ERROR: {error}')
			exit(0)
	ent_size = size

	#entropy = b'\x7f' * 16

	# generate the checksum length
	length = get_length(ent_size)

	# generate the SHA-256 digest of the entropy
	digest = sha_hash(entropy)

	# extract the checksum from the digest
	check = checksum(digest, length, ent_size * 8)
	
	print(f"9. Checksum: {bin(check)}")
	
	# append checksum to the entropy
	concat = concat_checksum(entropy, check);
	
	print(f'10. Concat: {bin(concat)}')
	
	# split buffer into groups of 11
	splits = split_digest(concat, ent_size)
	print(splits)
	# extract words from mnemonic word file
	words = gather_words()
	#for s in splits:
	#	print(bin(s))

	x = [words[s] for s in splits]

	seed = ' '.join(x)
	print(seed, end='\n\n')
	#salt = "mnemonicTREZOR"
	#hsh = pbkdf2_hmac('sha512', seed.encode('utf-8'), salt.encode('utf-8'), 2048, 64)
	#print(hexlify(hsh))
	return seed


if __name__ == "__main__":
	bip39((b'\xff' * 16), 16)
