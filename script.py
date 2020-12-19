from sys import exit, path
path.append('./src/')
from bip39 import bip39, generate_rootseed
from bip32 import generate_extended_keypair

def recover():
	''' Recover master keys from a mnemonic phrase '''
	pass

def generate():
	''' Generate a new BIP wallet on the fly '''
	size = input('Would you like a 12, 15, 18, 21, or 24 word passphrase? ')

	if size not in ['12', '15', '18', '21', '24']:
		raise Exception('Must select either 12, 15, 18, 21, or 24 words.')
	print(size)

def quit():
	''' Quit the BIP Suite CLI script '''
	exit(0)

def decode_wif():
	''' Decode a WIF-encoded key '''
	pass

def print_header():
	''' Print the BIP Suite ascii header '''
	print(' _______   __                   ______             __    __               \n|       \ |  \                 /      \           |  \  |  \              \n| $$$$$$$\ \$$  ______        |  $$$$$$\ __    __  \$$ _| $$_     ______  \n| $$__/ $$|  \ /      \       | $$___\$$|  \  |  \|  \|   $$ \   /      \ \n| $$    $$| $$|  $$$$$$\       \$$    \ | $$  | $$| $$ \$$$$$$  |  $$$$$$\\\n| $$$$$$$\| $$| $$  | $$       _\$$$$$$\| $$  | $$| $$  | $$ __ | $$    $$\n| $$__/ $$| $$| $$__/ $$      |  \__| $$| $$__/ $$| $$  | $$|  \| $$$$$$$$\n| $$    $$| $$| $$    $$       \$$    $$ \$$    $$| $$   \$$  $$ \$$     \\\n \$$$$$$$  \$$| $$$$$$$         \$$$$$$   \$$$$$$  \$$    \$$$$   \$$$$$$$\n              | $$                                                        \n              | $$                                                        \n               \$$                                                        \n')

def get_mode():
	''' Get the desired mode from the user '''
	return input('Would you like to:\n\n1). Generate a new BIP compatible wallet\n\n2). Recover master keys from a mnemonic phrase\n\n3). Exit BIP Suite\n\n$>  ')


def execute_mode(mode):
	''' Execute the high level internal functions 
		1) Generate BIP wallet
		2) Recover Master xprv/xpub keys
		3) Exit BIP Suite 
	'''
	if mode not in ['1', '2', '3']:
		raise Exception('Incorrect mode entered.')

	if mode == '1':
		generate()
	elif mode == '2':
		recover()
	quit()


def main():
	print_header()
	try:
		execute_mode(get_mode())
	except ValueError as e:
		print(f'There was an error: {e}')
		exit(1)


main()
