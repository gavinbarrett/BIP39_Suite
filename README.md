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
>>> from biptools.bip44 import BIP44

# use a valid BIP39 mnemonic phrase
>>> phrase = 'cactus fringe crater danger leave pill endorse night clown change apology issue'

# create a wallet
>>> wallet = BIP44(phrase)

# save a BIP44 path for Ethereum (coin type 60')
>>> path = "m/44'/60'/0'/0"

# generate the first ten hardened Ethereum addresses using the BIP44 path above
>>> addresses = wallet.gen_eth_addr_range(path, 10, True)

# print out the addresses
>>> for addr in addrs: print(addr)
0xf762e66c2589d54cee12d601a401ac70e6c98ac1
0x0612146e56fb06aca67117a5c9264981d2d4b2e3
0x79c80c5c454b3b5a3f27091ea8d13a3d0c6b6c0a
0x985c1f8caf2a25f18b384c36c2da9855c451a426
0x8f0be8b17bbdddfe56e57e6af7c1e315ab44b9b3
0xba6d031cf64239c47ad661f46bc850ae21d61e79
0xd397f885e1caa100570e89f85fa22f65c4e85199
0xdbeb23626d79c74f6c441f444e36fd92f4323071
0x832aa6003e99d521fcaa1a47895ec1bfe15a1980
0x5a97cac6132cbccc9724888707c9dc5d5fd82933
0xd69ae4119bb05942f82026aefe2b1d1e46dd2474
0xd747b7eae5f72e5d2b09882ea761a274554866d2
0x8a89cb3405dbd190f8a65ea6911b90b18fc369d4
0xbae1b2300f8b79b5ec409a0295d82c225dacf5e2
0x2e24df84eadec1415051c7526da1190feee1edd0
0x5f7040e45ca2dcc81fdd3b1c944c664de89e02e8
0x4df4179e4c1e0d5c9af8435dfff7c398d6735e69
0xd85a906e22eea199f092f462c262aefb6eec3074
0x3ffe184aa9775f1416d09e0e4fdf0cab53e65ae1
0x8a6ee897657356118578a7a55a25867ef3f32c42
```
