from src.entropy import *
from src.seeds import gather_words
from hashlib import pbkdf2_hmac
from binascii import hexlify
import unicodedata

#entropy = generate()

entropy = b'\x00' * 16

digest = sha_hash(entropy)

digest = bytes_to_int(digest)

check = checksum(digest)

concat = concat_checksum(entropy, check);

splits = split_digest(bytes_to_int(concat))

words = gather_words()

x = [words[s] for s in splits]


seed = ' '.join(x)
salt = "mnemonicTREZOR"

hsh = pbkdf2_hmac('sha512', seed.encode('utf-8'), salt.encode('utf-8'), 2048, 64)

print(seed)
print(hexlify(hsh))
