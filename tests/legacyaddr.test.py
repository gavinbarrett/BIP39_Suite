import json
import unittest
from sys import path
path.append('../')
from src.bip44 import BIP44

def load_data():
	f = open('test_vectors/legacy_vectors.json', 'r')
	data = f.read()
	f.close()
	addrs = json.loads(data)
	return [addr["addr"] for addr in addrs]

# load the legacy address test vectors
addrs = load_data()
path = "m/44'/0'/0'/0"

class TestLegacyDerivations(unittest.TestCase):
	
	def test_legacy_addr1(self):
		seed = '67f93560761e20617de26e0cb84f7234aaf373ed2e66295c3d7397e6d7ebe882ea396d5d293808b0defd7edd2babd4c091ad942e6a9351e6d075a29d4df872af'
		wallet = BIP44(seed, True)
		computed_addrs = wallet.gen_addr_range(path, 20)
		self.assertEqual(addrs, computed_addrs)

if __name__ == "__main__":
	unittest.main()
