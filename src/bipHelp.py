import hmac
from binascii import hexlify
from hashlib import sha512, pbkdf2_hmac

index = 0x00000000
public = 0x0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c200000000
chain = 0x873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508

'''
hmac_bytes = hmac.new(chain.to_bytes(32, 'big'), public.to_bytes(37, 'big'), sha512).hexdigest()
l = len(hmac_bytes)//2
print(hmac_bytes[:l])
print(hmac_bytes[l:])
'''
pb = pbkdf2_hmac('sha512', public.to_bytes(37, 'big'), chain.to_bytes(32, 'big'), 1, 64)
print(hexlify(pb))
