from os import urandom

def generate_chain():
	# return random 256-bit chain code
	return urandom(32)

