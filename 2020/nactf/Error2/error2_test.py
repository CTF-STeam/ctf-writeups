import random
from functools import reduce

#with open("flag.txt", "r") as fin:
#    flag = fin.read()
flag = 'test'

#with open("pos.txt", "r") as fin:
#    parity_pos = [int(i) for i in fin.read().split()]
parity_pos = [1, 1, 1, 1, 1, 1]

flag = "".join(str(format(ord(c), '08b')) for c in flag)  # converts flag to 8 bit ascii representation
print(flag)
flag = [[int(j) for j in flag[i:i + 11]] for i in range(0, len(flag), 11)]  # separates into 11 bit groups
print(flag)

code = []
for i in flag:
    print(i)
    for j in range(4):
        i.insert(2 ** j - 1, 0)
    print(i)
    parity = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(i) if bit])
    print(parity)
    parity = list(reversed(list(str(format(parity, "04b"))))) # separates number into individual binary bits
    print(parity)

    i = [k for j, k in enumerate(i) if j not in (0, 1, 3, 7)]
    print(i)

    for j in range(4):
        if parity[j] == "1":
            i.insert(parity_pos[j], 1)
        else:
            i.insert(parity_pos[j], 0)
    print(i)

    ind = random.randint(0, len(i) - 1)
    i[ind] = int(not i[ind]) # simulates a one bit error
    print(i)
    code.extend(i)

print(code)
enc = "".join([str(i) for i in code])
print(enc)
#with open("enc.txt", "w") as fout:
#    fout.write(enc)
