from binascii import hexlify
from json import loads, dumps
from flask import Flask, request, render_template
from biptools.bip39 import BIP39
from biptools.bip44 import BIP44
from biptools.bip49 import BIP49
from biptools.bip84 import BIP84

app = Flask(__name__)

def gen_wallet(seed, addr):
	if addr == "Legacy":
		return BIP44(seed)
	elif addr == "SegWit":
		return BIP49(seed)
	elif addr == "Native SegWit":
		return BIP84(seed)
	return None

def gen_keys(seed, addr):
	# determine path type (44/49/84)
	wallet = gen_wallet(seed.hex(), addr)
	if not wallet:
		return (None, None)
	# derive master key pair
	return wallet.get_master_keys()

@app.route('/generate', methods=['POST'])
def generate():
	data = request.data.decode('UTF-8')
	data = loads(data)
	try:
		bip39 = BIP39()
		# generate mnemonic passphrase
		mnemonics = bip39.bip39(data['bytes'])
		# extract address type
		addr = data['addr']
		# generate BIP32 root seed
		seed = bip39.generate_rootseed(mnemonics, data['passphrase'])
		prv, pub = gen_keys(seed, addr)
		if (prv, pub) == (None, None):
			return dumps({"phrase": "failed"})
		return dumps({"phrase": mnemonics, "seed": seed.hex(), "m_xprv": prv, "m_xpub": pub})
	except Exception as error:
		print(f'Could not generate: ERROR {error}')
		return dumps({"phrase": "failed"})

@app.route('/recover', methods=["POST"])
def recover():
	data = request.data.decode('UTF-8')
	data = loads(data)
	try:
		bip39 = BIP39()
		seed = bip39.generate_rootseed(data['mnemonics'], data['salt'])
		# FIXME: fix decoding error
		# extract address type
		addr = data["addr"]
		# generate a BIP32 wallet
		prv, pub = gen_keys(seed, addr)
		return dumps({"seed": seed.hex(), "m_xprv": prv, "m_xpub": pub})
	except Exception as error:
		print(f'Could not decode data.\nERROR: {error}')
		return dumps({"seed": "null"})

@app.route('/')
def serve_app():
	return render_template('./index.html')

if __name__ == "__main__":
	app.run(threaded=True, host='0.0.0.0')
