alphabet = 'abcdefghijklmnopqrstuvwxyz_!@'
flag = 'spbctf{'
seed = 5
for i in range(7, 23):
    flag += alphabet[seed]
    seed = seed * 3 % len(alphabet)
flag += '}'
print(flag)
