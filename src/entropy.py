from os import urandom
from hashlib import sha256
from sys import byteorder

def generate():
	# return 256 bits of entropy
	return urandom(32)

def sha_hash(entropy):
	# return the SHA-256 hash of the entropy
	hasher = sha256()
	hasher.update(entropy)
	return hasher.digest()

def bytes_to_int(digest):
	return int.from_bytes(digest, byteorder)

def checksum(entropy, digest):
	# return a checksum of our entropy
	integer = bytes_to_int(entropy)
	length = integer.bit_length()
	sumlength = length // 32
	print(f'length: {length}')
	print(f'sumlength: {sumlength}')
	num = integer >> (length - sumlength)
	print(num)
	return num.to_bytes(sumlength, byteorder)

def concat_checksum(entropy, checksum):
	# concatenate the checksum to the end of the entropy
	return entropy + checksum

def split_digest(digest):
	# split digest up into 24 11-bit numbers
	return [(digest >> idx) & 0x07ff for idx in range(0, digest.bit_length(), 11)]
