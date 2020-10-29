from sys import exit
from seeds import *
from entropy import *
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

	print(f'digest: {digest}')

	# extract the checksum from the digest
	check = checksum(digest, length)

	# append checksum to the entropy
	concat = concat_checksum(entropy, check);
	print(f'concat: {concat}')
	# split buffer into groups of 11
	splits = split_digest(bytes_to_int(concat), ent_size)

	# extract words from mnemonic word file
	words = gather_words()
	for s in splits:
		print(bin(s))

	x = [words[s] for s in splits]

	seed = ' '.join(x)
	print(seed)
	#salt = "mnemonicTREZOR"
	return seed
	#hsh = pbkdf2_hmac('sha512', seed.encode('utf-8'), salt.encode('utf-8'), 2048, 64)

	#print(hexlify(hsh))


if __name__ == "__main__":
	bip39((b'\xff' * 16), 16)
