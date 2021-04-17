from biptools.bip44 import BIP44

wallet = BIP44('b3db2b36e94a74fdd2cafc161c43ad5988bcf19219e2956f09155a5d1b68ad8ae47544899a1ef35e5788eb33e53351f6f865230125157a6565505a08e76cd911', True)

path = "m/44'/60'/0'/0"


'''
keys = wallet.derive_path(path)

prv_key = keys[-1]["prv"]
pub_key = keys[-1]["pub"]

child_prv, child_pub = wallet.derive_child_keys(prv_key, pub_key, b'\x04', 0)

ext_child_prv = wallet.extract_prv(child_prv)[0]

addr = wallet.derive_eth_address(ext_child_prv)

print(addr)
'''

addrs = wallet.gen_eth_addr_range(path, 20, False)
for addr in addrs:
	print(addr)
