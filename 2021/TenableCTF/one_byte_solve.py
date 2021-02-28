from pwn import *

HOST = 'challenges.ctfd.io'
PORT = 30468

flag = b''
octets = [16, 2, 119]
next = 0x64

def find_next_char(next):
	for octet in octets:
		c = octet ^ next
		r = remote(HOST, PORT)
		print(r.recvuntil('[flag]>'))
		r.sendline(flag + bytes([c]))
		resp = r.recvuntil('\r\n\r\n')
		print(resp)
		if b'You seem to know' in resp:
			next = r.recvuntil('\r\n\r\n').strip().decode()
			print('Next:' + next)
			return c, int(next[2:], 16)

while b'}' not in flag:
	c, next = find_next_char(next)
	flag += bytes([c])
	print(flag)
print(flag)
