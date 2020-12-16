import unittest
from sys import path
path.append('../src/')
from bip32 import generate_extended_keypair

class TestPubkeyGenerator():

	def test_pubkey_1(self):
		self.assertTrue(True)

if __name__ == "__main__":
	unittest.main()
