from src.entropy import *
from src.seeds import gather_words
from hashlib import pbkdf2_hmac

# generate entropy
#entropy = generate()
ent_size = 32

entropy = b'\x00' * 32

# generate the checksum length
length = get_length(ent_size)

# generate the SHA-256 digest of the entropy
digest = sha_hash(entropy)

# extract the checksum from the digest
check = checksum(digest, length)

# append checksum to the entropy
concat = concat_checksum(entropy, check);

# split buffer into groups of 11
splits = split_digest(bytes_to_int(concat), ent_size)

'''
# extract words from mnemonic word file
words = gather_words()


x = [words[s] for s in splits]

seed = ' '.join(x)
salt = "mnemonic"

hsh = pbkdf2_hmac('sha512', seed.encode('utf-8'), salt.encode('utf-8'), 2048, 64)

print(seed)
#print(hexlify(hsh))
'''
