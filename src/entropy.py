from os import urandom
from hashlib import sha256
from sys import byteorder
from binascii import b2a_hex, hexlify, unhexlify

def generate(n_bytes):
	# return n-bytes of entropy - either 16, 20, 24, 28, 32
	if n_bytes not in [16, 20, 24, 28, 32]:
		raise ValueError("Please select either 16, 20, 24, 28, or 32 bytes of entropy.")
	return urandom(n_bytes)

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

def unhex(x):
	if len(x) % 2:
		return unhexlify(b'0' + x)
	return x
	

def checksum(digest, length):
	# turn hex into readable stream
	hex_hash = hexlify(digest)
	print(hex_hash[:length//4])
	return unhexlify(pad_hex(hex_hash[:length//4]))

def concat_checksum(entropy, checksum):
	# concatenate the checksum to the end of the entropy
	print(f'entropy: {entropy}')
	print(f'checksum: {checksum}')
	return checksum + entropy

def split_digest(digest, ent_length):
	# split digest up into 24 11-bit numbers
	return [(digest >> idx) & 0x07ff for idx in range(0, ent_length * 8, 11)][::-1]
