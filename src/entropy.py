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

def bytes_to_int(digest):
	# return the hash as an integer
	return int.from_bytes(digest, byteorder)

def checksum(digest):
	# return a checksum of our entropy
	length = digest.bit_length()
	return digest >> (length - (length // 32))

def concat_checksum(entropy, checksum):
	# concatenate the checksum to the end of the entropy
	return entropy + checksum.to_bytes(1, byteorder)

def split_digest(digest):
	# split digest up into 24 11-bit numbers
	return [(digest >> idx) & 0x07ff for idx in range(0, digest.bit_length(), 11)]
