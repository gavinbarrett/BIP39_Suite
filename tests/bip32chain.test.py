from sys import path
import unittest
path.append('../src/')
from json import loads
from binascii import unhexlify
from bip32 import decode_path, generate_master_extended_keypair, generate_child_keypair

f = open('test_vectors/bip32chain.json', 'r')
data = loads(f.read())
f.close()


class BIPChainTester(unittest.TestCase):

	def test_chain_1(self):
		seed = data[0]["seed"]
		path = decode_path(data[0]["path"])
		keys = data[0]["keys"]
		# generate master key pair
		rootseed = unhexlify(seed)
		# generate master key pair
		xprv, xpub = generate_master_extended_keypair(rootseed)
		# check master keys
		self.assertEqual(xprv, keys[0]["prv"])
		self.assertEqual(xpub, keys[0]["pub"])
		for k in range(1, len(keys)):
			with self.subTest():
				# generate child key pair
				xprv, xpub = generate_child_keypair(xprv, xpub, k.to_bytes(1, 'big'), path[k])
				# check child keys
				self.assertEqual(xprv, keys[k]["prv"])
				self.assertEqual(xpub, keys[k]["pub"])

	def test_chain_2(self):
		seed = data[1]["seed"]
		path = decode_path(data[1]["path"])
		keys = data[1]["keys"]
		# generate master key pair
		rootseed = unhexlify(seed)
		# generate master key pair
		xprv, xpub = generate_master_extended_keypair(rootseed)
		# check master keys
		self.assertEqual(xprv, keys[0]["prv"])
		self.assertEqual(xpub, keys[0]["pub"])
		for k in range(1, len(keys)):
			with self.subTest():
				# generate child key pair
				xprv, xpub = generate_child_keypair(xprv, xpub, k.to_bytes(1, 'big'), path[k])
				# check child keys
				self.assertEqual(xprv, keys[k]["prv"])
				self.assertEqual(xpub, keys[k]["pub"])

	def test_chain_3(self):
		seed = data[2]["seed"]
		path = decode_path(data[2]["path"])
		keys = data[2]["keys"]
		# generate master key pair
		rootseed = unhexlify(seed)
		# generate master key pair
		xprv, xpub = generate_master_extended_keypair(rootseed)
		# check master keys
		self.assertEqual(xprv, keys[0]["prv"])
		self.assertEqual(xpub, keys[0]["pub"])
		for k in range(1, len(keys)):
			with self.subTest():
				# generate child key pair
				xprv, xpub = generate_child_keypair(xprv, xpub, k.to_bytes(1, 'big'), path[k])
				# check child keys
				self.assertEqual(xprv, keys[k]["prv"])
				self.assertEqual(xpub, keys[k]["pub"])


if __name__ == "__main__":
	unittest.main()
