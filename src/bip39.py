from entropy import *
from seeds import gather_words
from hashlib import pbkdf2_hmac

def bip39(entropy, size):
	# generate entropy
	if not entropy:
		entropy = generate(size)
	
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

	# split buffer into groups of 11
	splits = split_digest(bytes_to_int(concat), ent_size)

	# extract words from mnemonic word file
	words = gather_words()
	for s in splits:
		print(bin(s))

	x = [words[s] for s in splits]
	print(x)

	seed = ' '.join(x)
	#salt = "mnemonicTREZOR"
	return seed
	#hsh = pbkdf2_hmac('sha512', seed.encode('utf-8'), salt.encode('utf-8'), 2048, 64)

	#print(hexlify(hsh))


if __name__ == "__main__":
	bip39((b'\xff' * 32), 32)
