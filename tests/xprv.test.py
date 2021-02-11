from sys import path
import unittest
path.append('../src/')
from json import loads
from binascii import unhexlify
from bip32 import generate_secret, generate_extended_prvkey

f = open('vectors.json', 'r')
data = loads(f.read())['english']
f.close()

depth = b'\x00'
m_id = b'\x00' * 4

class XPrivKeyTest(unittest.TestCase):

	def test_xprv(self):
		for rkey, mphrase, seed, xprv in data:
			with self.subTest():
				# Generate BIP 32 root seed
				key, code = generate_secret(unhexlify(seed))
				# Generate a master xprv key
				xkey = generate_extended_prvkey(depth, m_id, m_id, key, code)
				# Check key derivation correctness
				self.assertEqual(xkey, xprv)
				print(f'{xprv}')


if __name__ == "__main__":
	unittest.main()
