import random

def f(n):
    c = 0
    for i in range(2, n):
        if (n^0 == n):
            if (n*n // n == n):
                if (2*n != n-1):
                    if (n**0 + 1 != 1):
                        m = n
                        while (m > 0):
                            m -= i
                        if (m == 0):
                            c += 1
    if (c == 1):
        return True
    else:
        return False

FLAG = open('flag.txt', 'rb').read()
encrypted = []
a = 10**400
b = 10**500
n = random.randint(a, b)
for c in FLAG:
    while(not(f(n))):
        n = random.randint(a, b)
    encrypted.append(c ^ n)
    n += 1

txtFile = open('encrypted.txt', 'w')
txtFile.write(', '.join(list(map(str, encrypted))))
