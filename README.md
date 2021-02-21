## Description
This repository presents a library for generating and managing hierarchical deterministic (HD) wallets. The core of this software includes an implementation of the BIP 39 and BIP 32 (Bitcoin Improvement Protocol) protocols for generating mnemonic seeds and wallets, respectively. The BIP 32 module contains the BIP32\_Account base class for deriving HD wallets based on the BIP 32 specification. It's recommended that you use the BIP44, BIP49, and BIP84 subclasses to generate HD wallets. These class make use of the BIP32\_Account core functionality but allow for deriving extended key pairs off of the 44', 49', and 84' purpose paths.

![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Build/badge.svg)


![](https://github.com/gavinbarrett/BIP39_Suite/workflows/BIP39%20Seed%20Generation/badge.svg)


![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Elliptic%20Curve%20Arithmetic/badge.svg)


![](https://github.com/gavinbarrett/BIP39_Suite/workflows/BIP32%20Path%20Derivation/badge.svg)

## Testing

You can test all of the BIP32/39 modules by running:
``./tests/run_tests.sh``
or run an individual test in the ``test`` directory. 

Running the last five test scripts in this file test requires having Python 3.8+ installed.

This will test 1) the generation of bits of entropy and a corresponding mnemonic recovery phrase for crypto wallets as well as a derived root seed used for deriving the BIP32 main node of the crypto wallet, 2) the correctness of secp256k1 elliptic curve arithmetic module, and 3) the derivation of a [base58check-encoded](https://en.bitcoin.it/wiki/Base58Check_encoding) master key pairs.

## Example

```python
from bipsuite import BIP44
seed = '000102030405060708090a0b0c0d0e0f'
wallet = BIP44(seed)
xprv, xpub = wallet.get_master_keys()
```
