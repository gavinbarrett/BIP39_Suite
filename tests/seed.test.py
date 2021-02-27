from sys import path
import unittest
path.append('../')
from json import loads
from src.bip39 import bip39, generate_rootseed
from hashlib import pbkdf2_hmac
from binascii import hexlify, unhexlify

f = open('vectors.json', 'r')
data = loads(f.read())['english']
f.close()

salt = "TREZOR"

class SeedTest(unittest.TestCase):

	def test_1_16bit_00(self):
		ent = unhexlify(data[0][0])
		mnemonics = bip39(16, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[0][2])
	
	def test_2_16bit_80(self):
		ent = unhexlify(data[1][0])
		mnemonics = bip39(16, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[1][2])

	def test_3_16bit_7f(self):
		ent = unhexlify(data[2][0])
		mnemonics = bip39(16, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[2][2])
	
	def test_4_16bit_ff(self):
		ent = unhexlify(data[3][0])
		mnemonics = bip39(16, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[3][2])


	def test_5_24bit_00(self):
		ent = unhexlify(data[4][0])
		mnemonics = bip39(24, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[4][2])
	
	def test_6_24bit_80(self):
		ent = unhexlify(data[5][0])
		mnemonics = bip39(24, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[5][2])
	
	def test_7_24bit_7f(self):
		ent = unhexlify(data[6][0])
		mnemonics = bip39(24, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[6][2])
	
	def test_8_24bit_ff(self):
		ent = unhexlify(data[7][0])
		mnemonics = bip39(24, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[7][2])

	def test_9_32bit_00(self):
		ent = unhexlify(data[8][0])
		mnemonics = bip39(32, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[8][2])
	
	def test_10_32bit_7f(self):
		ent = unhexlify(data[9][0])
		mnemonics = bip39(32, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[9][2])

	def test_11_32bit_80(self):
		ent = unhexlify(data[10][0])
		mnemonics = bip39(32, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[10][2])

	def test_12_32bit_ff(self):
		ent = unhexlify(data[11][0])
		mnemonics = bip39(32, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[11][2])


	def test_13_misc(self):
		size = len(data[12][0])//2
		ent = unhexlify(data[12][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[12][2])

	def test_14_misc(self):
		size = len(data[13][0])//2
		ent = unhexlify(data[13][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[13][2])
	
	def test_15_misc(self):
		size = len(data[14][0])//2
		ent = unhexlify(data[14][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[14][2])
	
	def test_16_misc(self):
		size = len(data[15][0])//2
		ent = unhexlify(data[15][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[15][2])

	def test_17_misc(self):
		size = len(data[16][0])//2
		ent = unhexlify(data[16][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[16][2])
	
	def test_18_misc(self):
		size = len(data[17][0])//2
		ent = unhexlify(data[17][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[17][2])

	def test_19_misc(self):
		size = len(data[18][0])//2
		ent = unhexlify(data[18][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[18][2])
	
	def test_20_misc(self):
		size = len(data[19][0])//2
		ent = unhexlify(data[19][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[19][2])
	
	def test_21_misc(self):
		size = len(data[20][0])//2
		ent = unhexlify(data[20][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[20][2])
	
	def test_22_misc(self):
		size = len(data[21][0])//2
		ent = unhexlify(data[21][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[21][2])
	
	def test_23_misc(self):
		size = len(data[22][0])//2
		ent = unhexlify(data[22][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[22][2])
	
	def test_24_misc(self):
		size = len(data[23][0])//2
		ent = unhexlify(data[23][0])
		mnemonics = bip39(size, ent)
		# check seed generation
		self.assertEqual(f'{generate_rootseed(mnemonics, salt).hex()}', data[23][2])

if __name__ == "__main__":
		unittest.main()
