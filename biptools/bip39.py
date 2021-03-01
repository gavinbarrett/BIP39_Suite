from biptools.seeds import Seeds
from biptools.entropy import Entropy
from sys import exit
from hashlib import pbkdf2_hmac
from binascii import hexlify

class BIP39:
	def __init__(self):
		# map desired mnemonic phrase length with bytes of entropy
		self.mnemonic_bytemap = {'12': 16, '15': 20, '18': 24, '21': 28, '24': 32}
		self.entropy = Entropy()
		self.words = Seeds().gather_words()

	def generate_entropy(self, size, entropy):
		# generate entropy
		if not entropy:
			try:
				entropy = self.entropy.generate(size)
				return entropy
			except ValueError as error:
				print(f'ERROR: {error}')
				exit(0)
		# return injected test case entropy
		return entropy

	def entropy_string(self, size, entropy):
		# return entropy bytes as a padded binary string
		return self.entropy.pad_string(bin(int.from_bytes(entropy, 'big'))[2:], size * 8)

	def bip39(self, size, entropy=None):
		# generate entropy
		entropy = self.generate_entropy(size, entropy)
		# generate the checksum length
		length = self.entropy.get_length(size)
		# generate the SHA-256 digest of the entropy
		digest = self.entropy.sha_hash(entropy)
		# turn entropy into a padded binary string 
		binary = self.entropy_string(size, entropy)
		# extract the checksum from the digest
		check = self.entropy.checksum(digest, length, size * 8)
		# append checksum to the entropy
		concat = binary + check
		# split buffer into groups of 11
		splits = self.entropy.split_entropy(size, concat)
		# interpret entropy strings as integers
		seeds = [self.words[int(s, 2)] for s in splits]
		return ' '.join(seeds)

	def generate_rootseed(self, mnemonics, salt):
		# return the seed generated from the mnemonic phrase
		return pbkdf2_hmac('sha512', mnemonics.encode('utf-8'), ('mnemonic' + salt).encode('utf-8'), 2048, 64)
