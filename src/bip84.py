import struct
from binascii import unhexlify
from secp256k1 import secp256k1, CurvePoint
from base58 import b58encode_check

# zprivate key version
z_prvkey_v = b'\x04\xb2\x43\x0c'
# zpublic key version
z_pubkey_v = b'\x04\xb2\x47\x46'

# set byte endianness
endianness = 'big'

class BIP84(BIP32_Account):
	def __init__(self):
		super().__init__(seed)
		pass
	
	def gen_child_zkeys(self, xprv, xpub, depth, index):
		# pass in parent xprv and xpub keys, depth, index to child_prvkey function
		index = struct.pack('>L', index)
		# generate child extended private key
		child_prv = self.generate_child_prvkey(xprv, xpub, depth, index, z_prvkey_v)
		# generate child extended public key
		child_pub = self.generate_child_pubkey(child_prv, xpub, depth, index, z_pubkey_v)
		return child_prv, child_pub

	def gen_bip84_path(self, path):
		#FIXME: define BIP 84 (bech32/native segwit addresses)
		''' Derive a BIP 84 path:
				m/84'/coin_type'/account'/change/address_index
		'''
		path_indices = self.decode_path(path)
		try:
			if len(path_indices) < 5:
				raise ValueError('BIP 44 path `{path_indices}` is not valid')
			if path_indices[1] != 0x8000002C:
				raise ValueError('BIP 44 purpose `{path_indices[1]}` is not valid')
			if not self.is_hardened(path_indices[2]):
				raise ValueError('BIP 44 coin_type `{path_indices[2]}` is not valid')
			if not self.is_hardened(path_indices[3]):
				raise ValueError('BIP 44 account number `{path_indices[3]}` is not valid')
			return self.generate_keypath(path_indices)
		except ValueError as err:
			print(f'Error occurred: {err}.')
