from pwn import *
from z3 import *

sv = Solver()
x = [None] * 1337
for i in range(1337):
    x[i] = Int('x' + str(i))
    sv.add(x[i] >= 0)

HOST = 'secretarray.fword.wtf'
PORT = 1337

s = remote(HOST, PORT)

print(s.recvuntil('START:\n').decode('utf-8'))

for i in range(1, 1337):
    s.send('0 ' + str(i) + '\n')
    sum2 = s.recvuntil('\n').decode('utf-8').rstrip()
    print('0 %s %s' % (i, sum2))
    sv.add(x[0] + x[i] == sum2)

s.send('1 2\n')
sum2 = s.recvuntil('\n').decode('utf-8').rstrip()
print('1 2 %s' % sum2)
sv.add(x[1] + x[2] == sum2)

#sv.add(x[0] + x[1] == 3)
#sv.add(x[1] + x[2] == 5)
#sv.add(x[0] + x[2] == 4)

print(sv.check())
m = sv.model()
print(m)

result = 'DONE'
for i in range(1337):
    #print(m[x[i]])
    result += ' ' + str(m[x[i]])
print(result)
s.send(result + '\n')
print(s.recv(100))
s.interactive()

