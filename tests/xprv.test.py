from sys import path
import unittest
path.append('../src/')
from json import loads
from binascii import unhexlify
from bip32 import generate_extended_prvkey

f = open('vectors.json', 'r')
data = loads(f.read())['english']
f.close()

class XPrivKeyTest(unittest.TestCase):

	def test_xpriv_1(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[0][2])).decode(), data[0][3])

	def test_xpriv_2(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[1][2])).decode(), data[1][3])
	
	def test_xpriv_3(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[2][2])).decode(), data[2][3])
	
	def test_xpriv_4(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[3][2])).decode(), data[3][3])
	
	def test_xpriv_5(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[4][2])).decode(), data[4][3])
	
	def test_xpriv_6(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[5][2])).decode(), data[5][3])
	
	def test_xpriv_7(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[6][2])).decode(), data[6][3])
	
	def test_xpriv_8(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[7][2])).decode(), data[7][3])
	
	def test_xpriv_9(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[8][2])).decode(), data[8][3])
	
	def test_xpriv_10(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[9][2])).decode(), data[9][3])
	
	def test_xpriv_11(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[10][2])).decode(), data[10][3])

	def test_xpriv_12(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[11][2])).decode(), data[11][3])
	
	def test_xpriv_13(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[12][2])).decode(), data[12][3])
	
	def test_xpriv_14(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[13][2])).decode(), data[13][3])
	
	def test_xpriv_15(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[14][2])).decode(), data[14][3])
	
	def test_xpriv_16(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[15][2])).decode(), data[15][3])
	
	def test_xpriv_17(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[16][2])).decode(), data[16][3])
	
	def test_xpriv_18(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[17][2])).decode(), data[17][3])
	
	def test_xpriv_19(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[18][2])).decode(), data[18][3])
	
	def test_xpriv_20(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[19][2])).decode(), data[19][3])
	
	def test_xpriv_21(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[20][2])).decode(), data[20][3])
	
	def test_xpriv_22(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[21][2])).decode(), data[21][3])
	
	def test_xpriv_23(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[22][2])).decode(), data[22][3])
	
	def test_xpriv_24(self):
		self.assertEqual(generate_extended_prvkey(unhexlify(data[23][2])).decode(), data[23][3])


if __name__ == "__main__":
	unittest.main()
