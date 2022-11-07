from string import ascii_lowercase
from random import seed, randbytes, choice

keys = []
for x in range(256):
    for a in ascii_lowercase:
        key = x.to_bytes(1, "big")
        key += a.encode("ascii")
        print(key)
        keys.append(key)
