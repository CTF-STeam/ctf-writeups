from pwn import *
import gmpy2
from gmpy2 import *

r = remote('35.222.104.86', 9001)

def send_pos(x, y):
	r.sendline(str(x) + ',' + str(y))

def get_distance():
	distance = r.recvuntil('\n')[10:].rstrip()
	print(distance)
	return mpfr(distance.decode('UTF-8'))

gmpy2.get_context().precision = 2048
flag = b''

for i in range(10000):
	r.recvuntil('1: ')
	x1, y1 = 0, 0
	send_pos(x1, y1)
	d1 = get_distance()
	#print(d1)

	r.recvuntil('2: ')
	x2, y2 = 1, 0
	send_pos(x2, y2)
	d2 = get_distance()
	#print(d2)

	r.recvuntil('3: ')
	x3, y3 = 0, 1
	send_pos(x3, y3)
	d3 = get_distance()
	#print(d3)

	x = (d1*d1 - d2*d2 + 1) / 2
	y = (d1*d1 - d3*d3 + 1) / 2
	print(x, y)
	if i > 10000:
		x = round(x, 1)
		y = round(y, 1)
	else:
		x = round(x)
		y = round(y)
	print(x, y, sqrt((x - x1)**2 + (y - y1)**2))

	send_pos(x, y)
	if i < 10000:
		print(i, r.recvuntil('something: '))
		bit = r.recvuntil('\n').rstrip()
		print(bit)
		flag = bit
		print(flag)
		if i >= 95:
			r.sendline('VoNguyenGiap')
			r.interactive()
	else:
		r.interactive()
