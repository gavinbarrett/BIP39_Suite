class secp256k1():
	# This class represents the secp256k1 elliptic curve: y^2 = x^3 + b (mod p)
	# Parameters sourced from https://en.bitcoin.it/wiki/Secp256k1
	def __init__(self):
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
		self.b = 0x0000000000000000000000000000000000000000000000000000000000000007
		self.x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
		self.y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
		self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

	def point_mult(self, p):
		# FIXME: perform EC point addition with secp256k1 parameters
		K = 0
		for i in range(p):
			K += (self.b) % self.n
