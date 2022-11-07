from pwn import *

password = "\\/[\\XZ_+YZ/\\]/].+`.ZW]XWW/*+,\\[Z"

for l in password[::-1]:
    x = 0x90 - ord(l)
    print(chr(x), end="")


# p = process("./nop")

# p.sendline("admin")
# p.sendline(pay)
# print(p.recvall())
