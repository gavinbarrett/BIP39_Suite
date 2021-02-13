# This script tests the correctness of deriving a BIP32 master node from a BIP39 master seed using pbkdf2_hmac.

import unittest
from sys import path
path.append('../src/')
from json import loads
from binascii import unhexlify
from bip39 import generate_rootseed
from bip32 import BIP32_Account

f = open('./vectors.json', 'r')
data = loads(f.read())['english']
f.close()

class MasterNodeTest(unittest.TestCase):

	def test_node_1(self):
		wallet = BIP32_Account(generate_rootseed(data[0][1], ''))
		print(wallet.rootseed)
		#print(generate_rootkey(data[0][1].encode()))

if __name__ == "__main__":
	unittest.main()
