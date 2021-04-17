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

# generate the first twenty hardened Ethereum addresses using the BIP44 path above
>>> addresses = wallet.gen_eth_addr_range(path, 20, True)

# print out the addresses
>>> for addr in addrs: print(addr)
0x8C82F03A9D205F08A51DE75C0BCC18392252B4D1
0x08D6FFFEF16C5BC20FFD3B71F3F08F116BA7D692
0x4DE6F5D61BF9184748C41CFFB9D8F378DA4B74DF
0xA8D015442470D215BE89C7B45803B8A193178498
0x5464017806A17BED623D7E2343C504A111610330
0x037BB37FF7029CFF101F06AA92D2962338992D01
0x22A9BE60CE7CB7D1951552204D3F38F48C634EC6
0x36FA3EE9B858E44DD8FC29FDAF13F8E7AA7F50FE
0xD4C5A267FD383BE02337AF89B7A0C864CA86110B
0x1C2545B2CEBF1CB2A80270B4E4FBC764349C35D9
0x449E4208309EDBCE8C653D5ED634EB9730A45122
0x989F181DF43626C71C33CDC5D79906C94173E5C8
0xD4BEDE7B7DD3B063D3E7238B84ED70262BA214E6
0xD554D9EBE348B83FB37A49AB81702A2560A11ADD
0xF02D89D10C8D7D6331537F8F92BE19E54C9C98D4
0x4C38D37037C7DC60F547B82EB3CDF1136ADFC44B
0x25A4E2F02543F0EA91E349FC0DBDA6F9B493D16F
0x0DF468517544FBE1156FD46328528482939E0218
0x48714A3778542ECFB4DDDD08F7DF1F2EC5253350
0xD34C2E85EE56C671FC9DC798804D3006887775C7
```
