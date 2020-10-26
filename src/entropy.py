from os import urandom
from hashlib import sha256
from sys import byteorder
from binascii import hexlify, unhexlify

def generate():
	# return bits of entropy - 16, 20, 24, 28, 32
	return urandom(32)

def sha_hash(entropy):
	# return the SHA-256 hash of the entropy
	hasher = sha256()
	hasher.update(entropy)
	return hasher.digest()

def bytes_to_int(digest):
	# convert bytes to integer
	return int.from_bytes(digest, byteorder)

def get_length(ent_size):
	# compute the length of the checksum
	return (ent_size * 8) // 32

def pad_hex(x):
	# pad any hex nibbles
	if len(x) % 2:
		return b'0' + x
	return x

def checksum(digest, length):
	# turn hex into readable stream
	hex_hash = hexlify(digest)
	x = pad_hex(hex_hash[:length//4])
	return unhexlify(x)

def concat_checksum(entropy, checksum):
	# concatenate the checksum to the end of the entropy
	return checksum + entropy[::-1]

def split_digest(digest, ent_length):
	# split digest up into 24 11-bit numbers
	return [(digest >> idx) & 0x07ff for idx in range(0, ent_length * 8, 11)][::-1]


