from sys import path
import unittest
path.append('../src/')
from json import loads
from binascii import unhexlify
from bip32 import generate_secret, generate_extended_prvkey

f = open('vectors.json', 'r')
data = loads(f.read())['english']
f.close()

class XPrivKeyTest(unittest.TestCase):

	def test_xpriv_1(self):
		key, code = generate_secret(unhexlify(data[0][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[0][3])

	def test_xpriv_2(self):
		key, code = generate_secret(unhexlify(data[1][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[1][3])
	
	def test_xpriv_3(self):
		key, code = generate_secret(unhexlify(data[2][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[2][3])
	
	def test_xpriv_4(self):
		key, code = generate_secret(unhexlify(data[3][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[3][3])
	
	def test_xpriv_5(self):
		key, code = generate_secret(unhexlify(data[4][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[4][3])
	
	def test_xpriv_6(self):
		key, code = generate_secret(unhexlify(data[5][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[5][3])
	
	def test_xpriv_7(self):
		key, code = generate_secret(unhexlify(data[6][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[6][3])
	
	def test_xpriv_8(self):
		key, code = generate_secret(unhexlify(data[7][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[7][3])
	
	def test_xpriv_9(self):
		key, code = generate_secret(unhexlify(data[8][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[8][3])
	
	def test_xpriv_10(self):
		key, code = generate_secret(unhexlify(data[9][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[9][3])
	
	def test_xpriv_11(self):
		key, code = generate_secret(unhexlify(data[10][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[10][3])

	def test_xpriv_12(self):
		key, code = generate_secret(unhexlify(data[11][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[11][3])
	
	def test_xpriv_13(self):
		key, code = generate_secret(unhexlify(data[12][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[12][3])
	
	def test_xpriv_14(self):
		key, code = generate_secret(unhexlify(data[13][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[13][3])
	
	def test_xpriv_15(self):
		key, code = generate_secret(unhexlify(data[14][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[14][3])
	
	def test_xpriv_16(self):
		key, code = generate_secret(unhexlify(data[15][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[15][3])
	
	def test_xpriv_17(self):
		key, code = generate_secret(unhexlify(data[16][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[16][3])
	
	def test_xpriv_18(self):
		key, code = generate_secret(unhexlify(data[17][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[17][3])
	
	def test_xpriv_19(self):
		key, code = generate_secret(unhexlify(data[18][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[18][3])
	
	def test_xpriv_20(self):
		key, code = generate_secret(unhexlify(data[19][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[19][3])
	
	def test_xpriv_21(self):
		key, code = generate_secret(unhexlify(data[20][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[20][3])
	
	def test_xpriv_22(self):
		key, code = generate_secret(unhexlify(data[21][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[21][3])
	
	def test_xpriv_23(self):
		key, code = generate_secret(unhexlify(data[22][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[22][3])
	
	def test_xpriv_24(self):
		key, code = generate_secret(unhexlify(data[23][2]))
		self.assertEqual(generate_extended_prvkey(key, code), data[23][3])


if __name__ == "__main__":
	unittest.main()
