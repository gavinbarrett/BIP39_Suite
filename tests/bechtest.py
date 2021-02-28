from src.bip44 import BIP44
from src.bip49 import BIP49
from src.bip84 import BIP84, bech32_create_checksum
from base58 import b58encode_check
from binascii import unhexlify

b39seed = '38f7ca4d0a0357794fd3fc6e9d6a4198c9ceba10eb0e118c1c745e8f23358562b9460fff45bdc28a539a117dc0a92167be1b6c08b1b7276be365baf377585e30'

mnemonic = 'later month erosion unfair drill refuse alley vicious patient risk kitten drink morning eyebrow delay offer creek hair library usual credit shock door broccoli'

wallet44 = BIP44(mnemonic)
wallet49 = BIP49(mnemonic)
wallet84 = BIP84(mnemonic)

path44 = "m/44'/0'/0'/0"
path49 = "m/49'/0'/0'/0"
path84 = "m/84'/0'/0'/0"

addrs44 = wallet44.gen_addr_range(path44, 10, True)
addrs49 = wallet49.gen_addr_range(path49, 10, True)
addrs84 = wallet84.gen_addr_range(path84, 10, True)

print('Legacy')
for addr in addrs44:
	print(addr)
print('\nSegWit')
for addr in addrs49:
	print(addr)
print('\nNative SegWit')
for addr in addrs84:
	print(addr)
