from binascii import unhexlify

class secp256k1():
	# This class represents the secp256k1 elliptic curve: y^2 = x^3 + b (mod p)
	# Parameters sourced from https://en.bitcoin.it/wiki/Secp256k1
	def __init__(self):
		self.x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
		self.y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
		self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
	
	def point_add(self, P, Q):
		# compute P + Q = R
		delta = ((Q[1] - P[1]) // (Q[0] - P[0])) % self.n
		x_r = ((delta**2) - P[0] - Q[0]) % self.n
		y_r = (delta * (P[0] - x_r) - P[1]) % self.n
		return (x_r, y_r)

	def point_double(self, P):
		delta = ((3 * P[0]**2) // (2 * P[1])) % self.n
		x_r = ((delta**2) - P[0] - self.x) % self.n
		y_r = (delta * (P[0] - x_r) - P[1]) % self.n
		return (x_r, y_r)

	def point_mult(self, privkey):
		# perform EC point addition with secp256k1 parameters K = kP
		P = (self.x, self.y)
		K = (0,0)
		xprv = int(privkey.hex(), 16) 
		for i in range(len(privkey)*8):
			if ((xprv >> i) & 0x01) == 0x01:
				K = self.point_add(K, P)
			P = self.point_double(P)
		return K

def trial():
	# run commands
	s = secp256k1()
	pubkey = s.point_mult(unhexlify('e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35'))
	eoo = pubkey[1] % 2
	nx = hex(pubkey[0])[2:]
	print(nx)
	if eoo == 1:
		return '03' + nx
	return '02' + nx

if __name__ == "__main__":
	expected_pubkey = '0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2'
	print(f'Expected: {expected_pubkey}\nComputed: {trial()}')
