#!/usr/bin/env bash

# Test BIP39 mnemonic phrase and root seed generation
python mnemonic.test.py
python seed.test.py

# Test elliptic curve arithmetic on secp256k1
python ellipticadd.test.py
python ellipticdouble.test.py
python ellipticmult.test.py

# Test deriving the base58-encoded master key pair
python xprv.test.py
python xpub.test.py
