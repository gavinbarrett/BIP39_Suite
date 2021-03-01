from os import urandom
from hashlib import sha256
from binascii import hexlify

class Entropy:
	def generate(self, n_bytes):
		# return n-bytes of entropy - either 16, 20, 24, 28, 32
		if n_bytes not in [16, 20, 24, 28, 32]:
			raise ValueError("Please select either 16, 20, 24, 28, or 32 bytes of entropy.")
		return urandom(n_bytes)

	def sha_hash(self, entropy):
		# return the SHA-256 hash of the entropy
		hasher = sha256()
		hasher.update(entropy)
		return hasher.digest()

	def get_length(self, ent_size):
		# compute the length of the checksum
		return (ent_size * 8) // 32

	def pad_string(self, binary, length):
		# ensure hash string is 256 chars
		return binary.zfill(length)

	def checksum(self, digest, length, num_bits):
		# turn hex into readable stream
		intsum = int(hexlify(digest), 16)
		# pad hash to multiple of 32
		padded = self.pad_string(bin(intsum)[2:], 256)
		# grab length number of bits
		return padded[:length]

	def split_entropy(self, ent_length, entropy):
		# split entropy up into 11-bit numbers
		return [entropy[i:i+11] for i in range(0, len(entropy), 11)]
