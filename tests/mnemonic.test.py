from sys import path
import unittest
path.append('../')
from json import loads
from src.bip39 import bip39
from hashlib import pbkdf2_hmac
from binascii import hexlify, unhexlify

f = open('vectors.json', 'r')
data = loads(f.read())['english']
f.close()


salt = "mnemonicTREZOR"
hsh = lambda mnemonics: pbkdf2_hmac('sha512', mnemonics.encode('utf-8'), salt.encode('utf-8'), 2048, 64)


class MnemonicTest(unittest.TestCase):

	def test_1_16bit_00(self):
		ent = unhexlify(data[0][0])
		mnemonics = bip39(16, ent)
		# check mnemonic generation
		self.assertEqual(mnemonics, data[0][1])

	def test_2_16bit_80(self):
		ent = unhexlify(data[1][0])
		mnemonics = bip39(16, ent)
		self.assertEqual(mnemonics, data[1][1])

	def test_3_16bit_7f(self):
		ent = unhexlify(data[2][0])
		mnemonics = bip39(16, ent)
		self.assertEqual(mnemonics, data[2][1])
	
	def test_4_16bit_ff(self):
		ent = unhexlify(data[3][0])
		mnemonics = bip39(16, ent)
		self.assertEqual(mnemonics, data[3][1])

	def test_5_24bit_00(self):
		ent = unhexlify(data[4][0])
		mnemonics = bip39(24, ent)
		self.assertEqual(mnemonics, data[4][1])
	
	def test_6_24bit_80(self):
		ent = unhexlify(data[5][0])
		mnemonics = bip39(24, ent)
		self.assertEqual(mnemonics, data[5][1])
	
	def test_7_24bit_7f(self):
		ent = unhexlify(data[6][0])
		mnemonics = bip39(24, ent)
		self.assertEqual(mnemonics, data[6][1])
	
	def test_8_24bit_ff(self):
		ent = unhexlify(data[7][0])
		mnemonics = bip39(24, ent)
		self.assertEqual(mnemonics, data[7][1])

	def test_9_32bit_00(self):
		ent = unhexlify(data[8][0])
		mnemonics = bip39(32, ent)
		self.assertEqual(mnemonics, data[8][1])
	
	def test_10_32bit_7f(self):
		ent = unhexlify(data[9][0])
		mnemonics = bip39(32, ent)
		self.assertEqual(mnemonics, data[9][1])

	def test_11_32bit_80(self):
		ent = unhexlify(data[10][0])
		mnemonics = bip39(32, ent)
		self.assertEqual(mnemonics, data[10][1])

	def test_12_32bit_ff(self):
		ent = unhexlify(data[11][0])
		mnemonics = bip39(32, ent)
		self.assertEqual(mnemonics, data[11][1])

	def test_13_misc(self):
		size = len(data[12][0])//2
		ent = unhexlify(data[12][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[12][1])

	def test_14_misc(self):
		size = len(data[13][0])//2
		ent = unhexlify(data[13][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[13][1])
	
	def test_15_misc(self):
		size = len(data[14][0])//2
		ent = unhexlify(data[14][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[14][1])
	
	def test_16_misc(self):
		size = len(data[15][0])//2
		ent = unhexlify(data[15][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[15][1])

	def test_17_misc(self):
		size = len(data[16][0])//2
		ent = unhexlify(data[16][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[16][1])
	
	def test_18_misc(self):
		size = len(data[17][0])//2
		ent = unhexlify(data[17][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[17][1])

	def test_19_misc(self):
		size = len(data[18][0])//2
		ent = unhexlify(data[18][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[18][1])
	
	def test_20_misc(self):
		size = len(data[19][0])//2
		ent = unhexlify(data[19][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[19][1])
	
	def test_21_misc(self):
		size = len(data[20][0])//2
		ent = unhexlify(data[20][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[20][1])
	
	def test_22_misc(self):
		size = len(data[21][0])//2
		ent = unhexlify(data[21][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[21][1])
	
	def test_23_misc(self):
		size = len(data[22][0])//2
		ent = unhexlify(data[22][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[22][1])
	
	def test_24_misc(self):
		size = len(data[23][0])//2
		ent = unhexlify(data[23][0])
		mnemonics = bip39(size, ent)
		self.assertEqual(mnemonics, data[23][1])


if __name__ == "__main__":
		unittest.main()
