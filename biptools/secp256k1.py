class CurvePoint:
	''' This class defines a point (x, y) over the curve secp256k1 '''	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

	def __add__(self, other):
		''' Add two points on the secp256k1 curve '''
		if self.x == 0 and self.y == 0:
			return CurvePoint(other.x, other.y)
		if other.x == 0 and other.y == 0:
			return CurvePoint(self.x, self.y)
		if self.x == other.x:
			return self.double()
		x1, y1 = self.x, self.y
		x2, y2 = other.x, other.y
		lam = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
		x_r = (pow(lam, 2, self.p) - x1 - x2) % self.p
		y_r = (lam * (x1 - x_r) - y1) % self.p
		return CurvePoint(x_r, y_r)

	def double(self):
		''' Double a point P on the secp256k1 curve '''
		x, y = self.x, self.y
		lam = (3 * pow(x, 2, self.p) * pow(2 * y, -1, self.p)) % self.p
		x_r = (pow(lam, 2, self.p) - x - self.x) % self.p
		y_r = (lam * (x - x_r) - y) % self.p
		return CurvePoint(x_r, y_r)
	
	def __mul__(self, xprv):
		P = self
		K = CurvePoint(0,0)
		while xprv:
			if xprv & 1:
				K = K + P
			P = P.double()
			xprv >>= 1
		return K
	
	def __rmul__(self, xprv):
		P = self
		K = CurvePoint(0,0)
		while xprv:
			if xprv & 1:
				K = K + P
			P = P.double()
			xprv >>= 1
		return K
	
	def __repr__(self):
		# return the point coordinates
		return f"({hex(self.x)}, {hex(self.y)})"


class secp256k1():
	# This class represents the secp256k1 elliptic curve: y^2 = x^3 + b (mod p)
	# Parameters sourced from https://en.bitcoin.it/wiki/Secp256k1
	def __init__(self):
		self.x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
		self.y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
		self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
		self.point = CurvePoint(self.x, self.y)
	
	def on_curve(self, point):
		# determine whether the point is on secp256k1
		return point.y**2 == point.x**3 + 7

	def generate_pubkey(self, privkey):
		# compute the public key from the private key through EC multiplication: K = nk
		return privkey * self.point
