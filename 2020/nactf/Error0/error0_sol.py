import binascii

with open('enc.txt') as f:
    line = f.readline()
ln = len(line) // 101
lines = [line[i*ln:i*ln+ln] for i in range(101)]

def find_max(i):
    count0 = 0
    count1 = 0
    for j in range(101):
        if lines[j][i] == '0':
            count0 += 1
        else:
            count1 += 1
    if count0 > count1:
        return '0'
    else:
        return '1'

flag = ''
for i in range(ln):
    flag += find_max(i)
flag = binascii.unhexlify('%x' % int(flag, 2))
print(flag)
