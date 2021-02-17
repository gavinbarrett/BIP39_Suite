from sys import exit, path
path.append('./src/')
from bip32 import generate_extended_keypair
from bip39 import bip39, generate_rootseed, mnemonic_bytemap

GREEN = '\033[92m'
SECRET = '\033[91m'
END = '\033[0m'

# FIXME: change interface to ask for passphrase the seed was salted with instead of prompting for the salt upon generation
def recover_from_phrase(mnemonic_phrase):
	''' Recover master keys from a mnemonic phrase '''
	# generate the user's wallet seed, salted with a passphrase if the user chooses to do so
	seed = generate_seed(mnemonic_phrase)
	print(f'Seed: {seed}\n')
	# generate the extended public/private key pair
	xprv, xpub = generate_extended_keypair(seed)
	# display the keys to the user
	display_keys(xprv, xpub)

def recover():
	''' Get the mnemonic phrase from the user ''' 
	mnemonic = input('\nPlease enter your mnemonic phrase\n\n$>  ')
	# FIXME: make sure the phrase is a valid length and all words are in the BIP39 wordlist
	recover_from_phrase(mnemonic)

def generate():
	''' Generate a new BIP wallet on the fly '''
	size = input('\nWould you like a 12, 15, 18, 21, or 24 word seed phrase? ')
	if size not in ['12', '15', '18', '21', '24']:
		raise Exception('Must select either 12, 15, 18, 21, or 24 words.')
	# generate the user's mnemonic phrase
	mnemonic_phrase = bip39(mnemonic_bytemap[size])
	# display the mnemonic phrase to the user
	display_mnemonic(mnemonic_phrase)
	# derive the root seed and extended key pair from the mnemonic phrase
	recover_from_phrase(mnemonic_phrase)

def generate_seed(mnemonic_phrase):
	''' Generate the seed from the mnemonic '''
	seed = None
	mode = input('Would you like to protect your generated wallet with a passphrase?\n\n1). Yes\n\n2). No\n\n$>  ')
	if mode == '1':
		seed = generate_rootseed(mnemonic_phrase, get_passphrase())
		print(f'\nYour salted root seed is {seed}\n')
	elif mode == '2':
		seed = generate_rootseed(mnemonic_phrase, '')
		print(f'\nYour root seed is {seed}\n')
	else:
		raise ValueError(f'Wrong mode {mode} given.')
	return seed	

def display_keys(xprv, xpub):
	''' Print the extended master key pair '''
	print(f'\nHere is your Master Extended Key Pair:\n\n{GREEN}{xprv}\n{xpub}{END}')

def display_mnemonic(mnemonic_phrase):
	''' Print the mnemonic phrase along with a warning message about its usage '''
	print(f'Your seed phrase is:\n\n{GREEN}{mnemonic_phrase}{END}\n\nWrite this down and {SECRET}keep it a secret{END}. It can be used to recover your entire crypto wallet tree and access your funds.\n\n')

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
	mode = input('Would you like to:\n\n1). Generate a new BIP compatible wallet\n\n2). Recover master keys from a mnemonic phrase\n\n3). Exit BIP Suite\n\n$>  ')
	if mode not in ['1', '2', '3']:
		raise ValueError(f'Wrong mode "{mode}" given.')
	return mode

def get_passphrase():
	''' Get the desired wallet passphrase '''
	inp1 = input('\nPlease enter your passphrase; the longer the better.\n\n$>  ')
	inp2 = input('\nPlease re-enter your passphrase.\n\n$>  ')
	if inp1 != inp2:
		raise ValueError('Given passphrases do not match.')
	return inp1

def execute_mode(mode):
	''' Execute the high level internal functions 
		1) Generate a BIP-compatible wallet?
		2) Recover BIP32 master keys?
		3) Exit BIP Suite?
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
		print(f'Error: {e}')
		exit(1)

if __name__ == "__main__":
	main()
