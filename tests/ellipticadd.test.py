import unittest
from sys import path
path.append('../src/')
from json import loads
from secp256k1 import secp256k1, CurvePoint

f = open('./test_vectors/ellipticvectors.json', 'r')
vects = loads(f.read())
f.close()

s = secp256k1()

g = CurvePoint(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

class TestEllipticPointAddition(unittest.TestCase):

	def test_case_1(self):
		k = int(vects[0]["k"])
		assert k == 1
		# extract starting point values
		x = int(vects[0]["x"], 16)
		y = int(vects[0]["y"], 16)
		# extract expected point values
		nX = int(vects[1]["x"], 16)
		nY = int(vects[1]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_2(self):
		k = int(vects[1]["k"])
		assert k == 2
		# extract starting point values
		x = int(vects[1]["x"], 16)
		y = int(vects[1]["y"], 16)
		# extract expected point values
		nX = int(vects[2]["x"], 16)
		nY = int(vects[2]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))


	def test_case_3(self):
		k = int(vects[2]["k"])
		assert k == 3
		# extract starting point values
		x = int(vects[2]["x"], 16)
		y = int(vects[2]["y"], 16)
		# extract expected point values
		nX = int(vects[3]["x"], 16)
		nY = int(vects[3]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_4(self):
		k = int(vects[3]["k"])
		assert k == 4
		# extract starting point values
		x = int(vects[3]["x"], 16)
		y = int(vects[3]["y"], 16)
		# extract expected point values
		nX = int(vects[4]["x"], 16)
		nY = int(vects[4]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_5(self):
		k = int(vects[4]["k"])
		assert k == 5
		# extract starting point values
		x = int(vects[4]["x"], 16)
		y = int(vects[4]["y"], 16)
		# extract expected point values
		nX = int(vects[5]["x"], 16)
		nY = int(vects[5]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_6(self):
		k = int(vects[5]["k"])
		assert k == 6
		# extract starting point values
		x = int(vects[5]["x"], 16)
		y = int(vects[5]["y"], 16)
		# extract expected point values
		nX = int(vects[6]["x"], 16)
		nY = int(vects[6]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_7(self):
		k = int(vects[6]["k"])
		assert k == 7
		# extract starting point values
		x = int(vects[6]["x"], 16)
		y = int(vects[6]["y"], 16)
		# extract expected point values
		nX = int(vects[7]["x"], 16)
		nY = int(vects[7]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_8(self):
		k = int(vects[7]["k"])
		assert k == 8
		# extract starting point values
		x = int(vects[7]["x"], 16)
		y = int(vects[7]["y"], 16)
		# extract expected point values
		nX = int(vects[8]["x"], 16)
		nY = int(vects[8]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_9(self):
		k = int(vects[8]["k"])
		assert k == 9
		# extract starting point values
		x = int(vects[8]["x"], 16)
		y = int(vects[8]["y"], 16)
		# extract expected point values
		nX = int(vects[9]["x"], 16)
		nY = int(vects[9]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_10(self):
		k = int(vects[9]["k"])
		assert k == 10
		# extract starting point values
		x = int(vects[9]["x"], 16)
		y = int(vects[9]["y"], 16)
		# extract expected point values
		nX = int(vects[10]["x"], 16)
		nY = int(vects[10]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_11(self):
		k = int(vects[10]["k"])
		assert k == 11
		# extract starting point values
		x = int(vects[10]["x"], 16)
		y = int(vects[10]["y"], 16)
		# extract expected point values
		nX = int(vects[11]["x"], 16)
		nY = int(vects[11]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_12(self):
		k = int(vects[11]["k"])
		assert k == 12
		# extract starting point values
		x = int(vects[11]["x"], 16)
		y = int(vects[11]["y"], 16)
		# extract expected point values
		nX = int(vects[12]["x"], 16)
		nY = int(vects[12]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_13(self):
		k = int(vects[12]["k"])
		assert k == 13
		# extract starting point values
		x = int(vects[12]["x"], 16)
		y = int(vects[12]["y"], 16)
		# extract expected point values
		nX = int(vects[13]["x"], 16)
		nY = int(vects[13]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))


	def test_case_14(self):
		k = int(vects[13]["k"])
		assert k == 14
		# extract starting point values
		x = int(vects[13]["x"], 16)
		y = int(vects[13]["y"], 16)
		# extract expected point values
		nX = int(vects[14]["x"], 16)
		nY = int(vects[14]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_15(self):
		k = int(vects[14]["k"])
		assert k == 15
		# extract starting point values
		x = int(vects[14]["x"], 16)
		y = int(vects[14]["y"], 16)
		# extract expected point values
		nX = int(vects[15]["x"], 16)
		nY = int(vects[15]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_16(self):
		k = int(vects[15]["k"])
		assert k == 16
		# extract starting point values
		x = int(vects[15]["x"], 16)
		y = int(vects[15]["y"], 16)
		# extract expected point values
		nX = int(vects[16]["x"], 16)
		nY = int(vects[16]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_17(self):
		k = int(vects[16]["k"])
		assert k == 17
		# extract starting point values
		x = int(vects[16]["x"], 16)
		y = int(vects[16]["y"], 16)
		# extract expected point values
		nX = int(vects[17]["x"], 16)
		nY = int(vects[17]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

	def test_case_18(self):
		k = int(vects[17]["k"])
		assert k == 18
		# extract starting point values
		x = int(vects[17]["x"], 16)
		y = int(vects[17]["y"], 16)
		# extract expected point values
		nX = int(vects[18]["x"], 16)
		nY = int(vects[18]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))
	
	def test_case_19(self):
		k = int(vects[18]["k"])
		assert k == 19
		# extract starting point values
		x = int(vects[18]["x"], 16)
		y = int(vects[18]["y"], 16)
		# extract expected point values
		nX = int(vects[19]["x"], 16)
		nY = int(vects[19]["y"], 16)
		# add point g to the starting point
		r = CurvePoint(x, y) + g
		self.assertEqual(hex(r.x), hex(nX))
		self.assertEqual(hex(r.y), hex(nY))

if __name__ == "__main__":
	unittest.main()
