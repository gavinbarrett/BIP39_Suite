from src.entropy import *
from src.seeds import gather_words

entropy = generate()

digest = sha_hash(entropy)

digest = bytes_to_int(digest)

check = checksum(digest)

concat = concat_checksum(digest, check);

splits = split_digest(bytes_to_int(concat))

words = gather_words()

x = [words[s] for s in splits]

for w in x:
	print(w, end=" ")
