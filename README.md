## Description
This is a Python3 implementation of the BIP39 and BIP32 protocols for handling Bitcoin keys and generating HD wallets.

![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Build/badge.svg)
![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Mnemonic%20Generation/badge.svg)
![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Seed%20Generation/badge.svg)
![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Elliptic%20Point%20Addition/badge.svg)
![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Elliptic%20Point%20Multiplication/badge.svg)
![](https://github.com/gavinbarrett/BIP39_Suite/workflows/xprv%20Derivation/badge.svg)
![](https://github.com/gavinbarrett/BIP39_Suite/workflows/xpub%20Derivation/badge.svg)

## Testing

You can test all of the BIP32/39 modules by running:
``./tests/run_tests.sh``
or run an individual test in the ``test`` directory. 

Running the last five test scripts in this file test requires having Python 3.8+ installed.

This will test 1) the generation of bits of entropy and a corresponding mnemonic recovery phrase for crypto wallets as well as a derived root seed used for deriving the BIP32 main node of the crypto wallet, 2) the correctness of secp256k1 elliptic curve arithmetic module, and 3) the derivation of a [base58check-encoded](https://en.bitcoin.it/wiki/Base58Check_encoding) master key pairs.
