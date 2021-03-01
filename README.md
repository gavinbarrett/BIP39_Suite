## Description
This repository presents a library for generating and managing hierarchical deterministic (HD) wallets. The core of this software includes an implementation of the BIP 39 and BIP 32 (Bitcoin Improvement Protocol) protocols for generating mnemonic seeds and wallets, respectively. The BIP 32 module contains the BIP32\_Account base class for deriving HD wallets based on the BIP 32 specification. It's recommended that you use the BIP44, BIP49, and BIP84 subclasses to generate HD wallets. These class make use of the BIP32\_Account core functionality but allow for deriving extended key pairs off of the 44', 49', and 84' purpose paths.

![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Build/badge.svg)


![](https://github.com/gavinbarrett/BIP39_Suite/workflows/BIP39%20Seed%20Generation/badge.svg)


![](https://github.com/gavinbarrett/BIP39_Suite/workflows/Elliptic%20Curve%20Arithmetic/badge.svg)


![](https://github.com/gavinbarrett/BIP39_Suite/workflows/BIP32%20Path%20Derivation/badge.svg)


## Installation

Install the ```bip-tools``` package in order to use this project programmatically.

```bash
pip install bip-tools
```


## Usage

```python
from biptools.bip44 import BIP44
phrase = 'cactus fringe crater danger leave pill endorse night clown change apology issue'
wallet = BIP44(phrase)
xprv, xpub = wallet.get_master_keys()
```
