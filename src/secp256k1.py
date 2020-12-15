from binascii import unhexlify
from tinyec.ec import SubGroup, Curve
from Crypto.Util.number import inverse

class Point():
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

	def __add__(self, other):
		x1, y1 = self.x, selfy
		x2, y2 = other.x, other.y
		if x1 == x2:
			return self.double()
			# FIXME: return
		delta = ((y2 - y1) * inverse(x2 - x1, self.p)) % self.p
		x_r = (pow(delta, 2, self.p) - x1 - x2) % self.p
		y_r = (delta * (x1 - x_r) - y1) % self.p
		return (x_r, y_r)

	def double(self):
		''' Double a point P on the secp256k1 curve '''
		x, y = self.x, self.y
		delta = (3 * pow(x, 2, self.p) * inverse(2 * y, self.p)) % self.p
		x_r = (pow(delta, 2, self.p) - x - self.x) % self.p
		y_r = (delta * (x - x_r) - y) % self.p
		return (x_r, y_r)


class secp256k1():

	# This class represents the secp256k1 elliptic curve: y^2 = x^3 + b (mod p)
	# Parameters sourced from https://en.bitcoin.it/wiki/Secp256k1
	def __init__(self):
		self.x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
		self.y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
		self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
	
	def point_add(self, P, Q):
		''' Add two points on secp256k1 '''
		x1, y1 = P
		x2, y2 = Q
		if x1 == x2:
			return self.point_double(P)
		# compute P + Q = R
		delta = ((y2 - y1) * inverse(x2 - x1, self.p)) % self.p
		x_r = (pow(delta, 2, self.p) - x1 - x2) % self.p
		y_r = (delta * (x1 - x_r) - y1) % self.p
		return (x_r, y_r)

	def point_double(self, P):
		''' Double a point P on the secp256k1 curve '''
		x, y = P
		delta = 3 * pow(x, 2, self.p) * inverse(2 * y, self.p)
		x_r = (pow(delta, 2, self.p) - x - x) % self.p
		y_r = (delta * (x - x_r) - y) % self.p
		return (x_r, y_r)

	def __rmul__(self, xprv):
		K = (0,0)
		P = (self.x, self.y)
		#print(f'P: ({hex(P[0])}, {hex(P[1])})')
		#print(f'xprv: {xprv}')
		while xprv:
			#print(f'Mult by: {xprv}')
			if xprv & 1:
				#print(f'pre-K: ({hex(K[0])}, {hex(K[1])})')
				K = self.point_add(K, P)
				#print(f'post-K: ({hex(K[0])}, {hex(K[1])})')
			P = self.point_double(P)
			#print(f'pre-P: ({hex(P[0])}, {hex(P[1])})')
			#print(f'post-P: ({hex(P[0])}, {hex(P[1])})')
			xprv >>= 1
		return K

def test_mult():
	
	s = secp256k1()
	xprv = 'e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35'
	#xprv = '02'
	pubkey = int(xprv, 16) * s
	print('\n')
	print(hex(pubkey[0]))
	x = hex(pubkey[0])[2:]
	if pubkey[1] & 1:
		return '03' + x
	return '02' + x
'''
	privkey = int('e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35', 16)
	field = SubGroup(p=s.p, g=(s.x, s.y), n=s.n, h=1) 
	curve = Curve(a=0, b=7, field=field, name='secp256k1')
	pubkey = privkey * curve.g
	if pubkey.y & 1:
		return '03' + hex(pubkey.x)[2:]
	return '02' + hex(pubkey.x)[2:]
'''	

if __name__ == "__main__":
	#test_mult()
	expected_pubkey = '0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2'
	print(f'Expected: {expected_pubkey}\nComputed: {test_mult()}')
