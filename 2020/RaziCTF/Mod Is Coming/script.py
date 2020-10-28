import random
from numpy import *
from PIL import Image
from functools import reduce


def f1(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * f3(p, n_i) * p
    return sum % prod


def f2(a, b): 
    if b == 0: 
        return a 
    else: 
        return f2(b, a%b) 


def f3(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def encrypt(s):
    c_p = []
    for i in range(10,21):
        for j in range(i+1,21):
            if f2(i,j) == 1:
                c_p.append([i,j])
    rand = random.randint(0,len(c_p))
    k = f1(c_p[rand], [len(s), len(s)*3])
    while k == 0:
        rand = random.randint(0,len(c_p))
        k = f1(c_p[rand], [len(s), len(s)*3])
    img = Image.new('RGB', (len(s)*3, len(s)), color = 'white')
    image = array(img)
    x, y, z = image.shape
    for a in range (0, x):
        for b in range (0, y):
            p = image[a, b]
            p[0] = ((k-10) * ord(s[a])) % 251
            p[1] = (k * ord(s[a])) % 251
            p[2] = ((k+10) * ord(s[a])) % 251
            image[a][b] = p
    enc = Image.fromarray(image)
    enc.save('enc.png')


f = open("secretmsg.txt", "r")
encrypt(f.read())