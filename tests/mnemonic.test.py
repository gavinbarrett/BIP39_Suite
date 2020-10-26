from sys import path
import unittest
path.append('../src/')
from bip39 import bip39

class MnemonicTest(unittest.TestCase):

	def test_16bit_00(self):
		ent = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		self.assertEqual(bip39(ent, 16), "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about")
	
	def test_16bit_80(self):
		ent = b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
		self.assertEqual(bip39(ent, 16), "letter advice cage absurd amount doctor acoustic avoid letter advice cage above")
	
	def test_16bit_7f(self):
		ent = b'\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f'
		self.assertEqual(bip39(ent, 16), "legal winner thank year wave sausage worth useful legal winner thank yellow")
	
	def test_16bit_ff(self):
		ent = b'\xff' * 32
		self.assertEqual(bip39(ent, 32), "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong")


	def test_24bit_00(self):
		ent = b'\x00' * 24
		self.assertEqual(bip39(ent, 24), "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon agent")
	
	def test_24bit_80(self):
		ent = b'\x80' * 24
		self.assertEqual(bip39(ent, 24), "letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter always")
	
	def test_24bit_7f(self):
		ent = b'\x7f' * 24
		self.assertEqual(bip39(ent, 24), "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal will")
	
	def test_24bit_ff(self):
		ent = b'\xff' * 24
		self.assertEqual(bip39(ent, 24), "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo when")


	def test_32bit_00(self):
		ent = b'\x00' * 32
		self.assertEqual(bip39(ent, 32), "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art")

	def test_32bit_80(self):
		ent = b'\x80' * 32
		self.assertEqual(bip39(ent, 32), "letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic bless")

	def test_32bit_7f(self):
		ent = b'\x7f' * 32
		self.assertEqual(bip39(ent, 32), "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legalwinner thank year wave sausage worth title")

	def test_32bit_ff(self):
		ent = b'\xff' * 32
		self.assertEqual(bip39(ent, 32), "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo vote")


if __name__ == "__main__":
	unittest.main()
