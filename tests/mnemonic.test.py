from sys import path
import unittest
path.append('../src/')
from json import loads
from bip39 import bip39
from binascii import unhexlify
f = open('vectors.json', 'r')
data = loads(f.read())['english']
f.close()
print(data)

class MnemonicTest(unittest.TestCase):

	def test_16bit_00(self):
		ent = unhexlify(data[0][0])
		mnemonics = bip39(ent, 16)
		self.assertEqual(mnemonics, data[0][1])
	
	def test_16bit_80(self):
		ent = unhexlify(data[1][0])
		mnemonics = bip39(ent, 16)
		self.assertEqual(mnemonics, data[1][1])
	
	def test_16bit_7f(self):
		ent = unhexlify(data[2][0])
		mnemonics = bip39(ent, 16)
		self.assertEqual(mnemonics, data[2][1])
	
	def test_16bit_ff(self):
		ent = unhexlify(data[3][0])
		mnemonics = bip39(ent, 16)
		self.assertEqual(mnemonics, data[3][1])


	def test_24bit_00(self):
		ent = unhexlify(data[4][0])
		mnemonics = bip39(ent, 24)
		self.assertEqual(mnemonics, data[4][1])
	
	def test_24bit_80(self):
		ent = unhexlify(data[5][0])
		mnemonics = bip39(ent, 24)
		self.assertEqual(mnemonics, data[5][1])
	
	def test_24bit_7f(self):
		ent = unhexlify(data[6][0])
		mnemonics = bip39(ent, 24)
		self.assertEqual(mnemonics, data[6][1])
	
	def test_24bit_ff(self):
		ent = unhexlify(data[7][0])
		mnemonics = bip39(ent, 24)
		self.assertEqual(mnemonics, data[7][1])


	def test_32bit_00(self):
		ent = unhexlify(data[8][0])
		mnemonics = bip39(ent, 32)
		self.assertEqual(mnemonics, data[8][1])

	def test_32bit_80(self):
		ent = unhexlify(data[9][0])
		mnemonics = bip39(ent, 32)
		self.assertEqual(mnemonics, data[9][1])

	def test_32bit_7f(self):
		ent = unhexlify(data[10][0])
		mnemonics = bip39(ent, 32)
		self.assertEqual(mnemonics, data[10][1])

	def test_32bit_ff(self):
		ent = unhexlify(data[11][0])
		mnemonics = bip39(ent, 32)
		self.assertEqual(mnemonics, data[11][1])

	
if __name__ == "__main__":
		unittest.main()
