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

def get_length(ent_size):
	# compute the length of the checksum
	return (ent_size * 8) // 32

def mask(length):
	# return a set mask of an arbitrary length
	return int(('1' * length), 2)

def pad(binary):
	# pad hash to 256 bits
	return binary.zfill(256)

def pad_checksum(bits):
	# return checksum padded to an even number of nibbles
	if len(bits) % 2:
		return bits.zfill(len(bits) + 1)
	return bits

def checksum(digest, length, num_bits):
	# turn hex into readable stream
	intsum = int(hexlify(digest), 16)
	
	# pad to multiple of 32
	padded = pad(bin(intsum)[2:])
	print(f'1. Hash: {bin(intsum)}')
	print(f'2. Padded Hash: {padded}')
	print(f'3. Length: {length}')
	print(f'4. Num_bits: {num_bits}')
	print(f'5. Stripping {length} bits')
	print(f'6. Shift Amount: {num_bits-length}')
	# FIXME: AND shifted intsum with a dynamically constructed mask
	#i = (intsum >> (num_bits - length)) & mask(length)

	# grab length number of bits
	bits = padded[:length]
	print(f'7. Bits: {bits}')
	pad_bits = pad_checksum(bits)
	print(f'8. Checksum: {int(bits, 2)}')
	return int(bits, 2)

def concat_checksum(entropy, checksum):
	# concatenate the checksum to the end of the entropy
	intropy = int(hexlify(entropy), 16)
	return (intropy << checksum.bit_length()) | checksum

def split_digest(digest, ent_length):
	# split digest up into 24 11-bit numbers
	return [(digest >> idx) & 0x07ff for idx in range(0, ent_length * 8, 11)][::-1]
