from pwn import *
import base64
import imageId

r = remote("io.ept.gg", 30049)
a = r.recvuntil("ready?\n".encode())
r.sendline()
for _ in range(401):
    out = b""
    try:
        out += r.recvuntil("Where is the ".encode())
    except:
        out += r.recvline()
        out += r.recvline()
        out += r.recvline()
        out += r.recvline()
        print(out)
    shape = r.recvuntil(" ([").decode()[:-3]
    out += shape.encode()
    print("SHAPE: " + shape)
    out += r.recvuntil(")?\n".encode())
    b = r.recvuntil("\n".encode())
    out += b

    filename = "out.png"

    with open(filename, "wb") as file:
        b = base64.b64decode(b)
        file.write(b)

    pos = imageId.findShape(filename, shape).lower().encode()
    print("JEG SENDER: ", pos)
    r.sendline(pos)
    try:
        out += r.recvuntil("Correct!\n".encode())
    except:
        print(out)
        print(r.recvuntil("\n"))
        print(r.recvuntil("\n"))
        print(r.recvuntil("\n"))
        print(r.recvuntil("\n"))

print(r.recvuntil("\n"))
print(r.recvuntil("\n"))
print(r.recvuntil("\n"))
print(r.recvuntil("\n"))
print(r.recvuntil("\n"))
