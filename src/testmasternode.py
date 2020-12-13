import hmac
from binascii import unhexlify
from hashlib import pbkdf2_hmac, sha512

seed = unhexlify('a83930217f6671af4a1a1bcef98f41c52d0ea70bed8d92b7fbdb8d531efa6d312fe2e2a15acf743387072bdace60cba2846449527f1f8f793fc6abd7d854ae8d')

#res = pbkdf2_hmac('sha512', seed, b'Bitcoin seed', 2048, 64)
res = hmac.new(b'Bitcoin seed', seed, sha512).hexdigest()
print(f'Res: {res}')
privkey = res[:len(res)//2]
chaincode = res[len(res)//2:]

print(f'Computed Private Key:  {privkey}\nComputed Chain Code:   {chaincode}\n')

exp = '0488ade400000000000000000044aed744c1c30eb0298c1586eac257de5f27af381a6842059360dfd89c8055af00582badc354dcfff186212d43aa1b02cfe1a51c37e012a78bd77b2f6bdee3bebeeda25f5a'

# strip metadata
e = exp[26:]
# strip checksum
e = e[:-8]

# extract expected chain code and master key
exp_chaincode = e[:64]
exp_privkey = e[66:]

print(f'Expected private key:  {exp_privkey}\nExpected chain code:   {exp_chaincode}')
