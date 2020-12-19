from sys import path
path.append('./src/')
from binascii import hexlify
from json import loads, dumps
from flask import Flask, request, render_template
from bip39 import bip39, generate_rootseed
from bip32 import generate_rootkey

app = Flask(__name__)

@app.route('/generate', methods=["POST"])
def generate():
	data = request.data.decode('UTF-8')
	data = loads(data)
	try:
		print(data)
		mnemonics = bip39(data['bytes'])
		print(mnemonics)
		seed = generate_rootseed(mnemonics, data["passphrase"])
		print(seed)
		node = generate_rootkey(seed)
		print(node)
		return dumps({"phrase": mnemonics, "seed": seed.decode(), "node": node})
	except Exception as error:
		print(f'Could not generate: ERROR {error}')
		return dumps({"phrase": "failed"})

@app.route('/recover', methods=["POST"])
def recover():
	data = request.data.decode('UTF-8')
	data = loads(data)
	try:
		seed = generate_rootseed(data['mnemonics'], data['salt'])
		return dumps({"seed": seed})
	except Exception as error:
		print(f'Could not decode data.\nERROR: {error}')
		return dumps({"seed": "null"})

@app.route('/')
def serve_app():
	return render_template('./index.html')

if __name__ == "__main__":
	app.run(threaded=True, host='0.0.0.0')
