from os import urandom
from hashlib import sha256
from sys import byteorder

def generate():
	# return 256 bits of entropy
	return urandom(16)

def sha_hash(entropy):
	# return the SHA-256 hash of the entropy
	hasher = sha256()
	hasher.update(entropy)
	return hasher.digest()

def hash_to_int(digest):
	# return the hash as an integer
	return int.from_bytes(digest, byteorder)

def checksum(digest):
	# return a checksum of our entropy
	return digest >> (digest.bit_length() - 8)

entropy = generate()
digest = sha_hash(entropy)
digest = hash_to_int(digest)
check = checksum(digest)
print(check)
