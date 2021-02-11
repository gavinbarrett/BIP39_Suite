import unittest
from sys import path
path.append('../src/')
from binascii import unhexlify
from bip32 import generate_extended_pubkey

depth = b'\x00'
m_id = b'\x00' * 4

class TestPubkeyGenerator(unittest.TestCase):

	def test_pubkey_1(self):
		secretkey = unhexlify('edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea')
		chaincode = unhexlify('47fdacbd0f1097043b78c63c20c34ef4ed9a111d980047ad16282c7ae6236141')
		exp = 'xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8'
		self.assertTrue(exp, generate_extended_pubkey(depth, m_id, m_id, secretkey, chaincode))
	
	def test_pubkey_2(self):
		secretkey = unhexlify('4b03d6fc340455b363f51020ad3ecca4f0850280cf436c70c727923f6db46c3e')
		chaincode = unhexlify('60499f801b896d83179a4374aeb7822aaeaceaa0db1f85ee3e904c4defbd9689')
		exp = 'xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB'
		self.assertTrue(exp, generate_extended_pubkey(depth, m_id, m_id, secretkey, chaincode))

if __name__ == "__main__":
	unittest.main()
