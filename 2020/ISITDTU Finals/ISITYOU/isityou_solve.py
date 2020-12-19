#!/usr/bin/env python3
from Crypto.Util.number import *
import os
from hashlib import sha256
from random import randint
import string
import threading
import socketserver
import string

FLAG = 'isitdtu{123456}'
great_poem = open('my_poem.txt').read()
print(great_poem)

def find_maxh(o, start):
    maxh = 0
    for h in range(start, 256, 1 << (o+1)):
        maxh = h
        #print(h)
    return maxh

#find_maxh(2)

def find_maxn(h, t):
    maxn = 0
    for n in range(h, t+h, 2):
        maxn = n
        #print(h)
    return maxn

# What the heck?
WTF = ord('c')*11
WTF += ord('o')*9
WTF += ord('t')*5
WTF += ord('h')*3
WTF += ord('A')*2
WTF += ord('n')*2
print(WTF)

# Transform
def isitme(r):
    if len(r) != 256:
        return False

    _a = [1, 17, 289, 1584, 296, 1703, 2319, 2804, 1062, 1409, 650, 1063, 1426, 939,
          2647, 1722, 2642, 1637, 1197, 375, 3046, 1847, 1438, 1143, 2786, 756, 2865, 2099,
          2393, 733, 2474, 2110, 2580, 583, 3253, 2037, 1339, 2789, 807, 403, 193, 3281,
          2513, 2773, 535, 2437, 1481, 1874, 1897, 2288, 2277, 2090, 2240, 1461, 1534,
          2775, 569, 3015, 1320, 2466, 1974, 268, 1227, 885, 1729, 2761, 331, 2298, 2447,
          1651, 1435, 1092, 1919, 2662, 1977, 319, 2094, 2308, 2617, 1212, 630, 723, 2304,
          2549, 56, 952, 2868, 2150, 3260, 2156, 33, 561, 2879, 2337, 3110, 2935, 3289,
          2649, 1756, 3220, 1476, 1789, 452, 1026, 797, 233, 632, 757, 2882, 2388, 648,
          1029, 848, 1100, 2055, 1645, 1333, 2687, 2402, 886, 1746, 3050, 1915, 2594, 821,
          641, 910, 2154]
    print(len(_a))

    c = 1
    for o in range(7, 0, -1):
        t = 1 << o
        #print(t)
        for h in range(0, 256, 1 << (o+1)):
            a = _a[c]
            #print(a)
            for n in range(h, t+h, 2):
                co = n + t
                th = n

                an = (a * r[co]) % (WTF - 1)
                r[co] = (r[th] - an) % (WTF - 1)
                r[th] = (r[th] + an) % (WTF - 1)

            c += 1
            #print(c)
    print(r)
    c = 1
    for o in range(7, 0, -1):
        t = 1 << o
        for h in range(1, 256, 1 << (o+1)):
            a = _a[c]
            for n in range(h, t+h, 2):
                co = n + t
                th = n

                if co == 255:
                    print('i', a, co, th, r[co], r[th])

                an = (a * r[co]) % (WTF - 1)
                r[co] = (r[th] - an) % (WTF - 1)
                r[th] = (r[th] + an) % (WTF - 1)

                if co == 255:
                    print('i', a, co, th, r[co], r[th])
            c += 1
            #print(c)
    print(r)

    return True

def test(a, co, th):
    an = (a * co) % (WTF - 1)
    print(an)
    co = (th - an) % (WTF - 1)
    th = (th + an) % (WTF - 1)
    print(co, th)

def rev(a, co, th):
    _th = ((co + th) % (WTF - 1) * inverse(2, WTF - 1)) % (WTF - 1)
    #print(_th)
    an = ((th - co) % (WTF - 1) * inverse(2, WTF - 1)) % (WTF - 1)
    #print(an)
    _co = (an * inverse(a, WTF - 1)) % (WTF - 1)
    #print(_co, _th)
    return _co, _th

def solve(r):
    _a = [1, 17, 289, 1584, 296, 1703, 2319, 2804, 1062, 1409, 650, 1063, 1426, 939,
          2647, 1722, 2642, 1637, 1197, 375, 3046, 1847, 1438, 1143, 2786, 756, 2865, 2099,
          2393, 733, 2474, 2110, 2580, 583, 3253, 2037, 1339, 2789, 807, 403, 193, 3281,
          2513, 2773, 535, 2437, 1481, 1874, 1897, 2288, 2277, 2090, 2240, 1461, 1534,
          2775, 569, 3015, 1320, 2466, 1974, 268, 1227, 885, 1729, 2761, 331, 2298, 2447,
          1651, 1435, 1092, 1919, 2662, 1977, 319, 2094, 2308, 2617, 1212, 630, 723, 2304,
          2549, 56, 952, 2868, 2150, 3260, 2156, 33, 561, 2879, 2337, 3110, 2935, 3289,
          2649, 1756, 3220, 1476, 1789, 452, 1026, 797, 233, 632, 757, 2882, 2388, 648,
          1029, 848, 1100, 2055, 1645, 1333, 2687, 2402, 886, 1746, 3050, 1915, 2594, 821,
          641, 910, 2154]
    c = 127
    for o in range(1, 8):
        t = 1 << o
        #print(t)
        for h in range(find_maxh(o, 1), 0, -(1 << (o+1))):
            #print(h)
            a = _a[c]
            for n in range(find_maxn(h, t), h - 1, -2):
                co = n + t
                th = n

                if co == 255:
                    print('s', a, co, th, r[co], r[th])

                r[co], r[th] = rev(a, r[co], r[th])

                if co == 255:
                    print('s', a, co, th, r[co], r[th])
            c -= 1
            #print(c)
    print(r)

    c = 127
    for o in range(1, 8):
        t = 1 << o
        #print(t)
        for h in range(find_maxh(o, 0), -1, -(1 << (o+1))):
            a = _a[c]
            #print(a)
            for n in range(find_maxn(h, t), h - 1, -2):
                co = n + t
                th = n

                r[co], r[th] = rev(a, r[co], r[th])
            c -= 1
    print('-' * 68)
    print("Solution:")
    print(r)

r = [ord(c) for c in great_poem]
print(r)
print(len(r))
test(17, 123, 456)
print(rev(17, 1694, 2547))
#1694 2547

#r = [416, 416, 3129, 3129, 374, 374, 887, 887, 923, 923, 3314, 3314, 597, 597, 3, 3, 1484, 1484, 2945, 2945, 1510, 1510, 2909, 2909, 84, 84, 2290, 2290, 3022, 3022, 477, 477, 142, 142, 1807, 1807, 846, 846, 681, 681, 2715, 2715, 2256, 2256, 2094, 2094, 291, 291, 536, 536, 3186, 3186, 3012, 3012, 2191, 2191, 403, 403, 1553, 1553, 1222, 1222, 3226, 3226, 2725, 2725, 1404, 1404, 263, 263, 2892, 2892, 2450, 2450, 159, 159, 1570, 1570, 1943, 1943, 581, 581, 3002, 3002, 591, 591, 1838, 1838, 2296, 2296, 3252, 3252, 2996, 2996, 1447, 1447, 2848, 2848, 1768, 1768, 1374, 1374, 2623, 2623, 1628, 1628, 426, 426, 2865, 2865, 3199, 3199, 1956, 1956, 1735, 1735, 1744, 1744, 6, 6, 2104, 2104, 320, 320, 219, 219, 2931, 2931, 1090, 1090, 732, 732, 193, 193, 2905, 2905, 712, 712, 617, 617, 625, 625, 1891, 1891, 2948, 2948, 2995, 2995, 996, 996, 943, 943, 2628, 2628, 426, 426, 504, 504, 1202, 1202, 947, 947, 2351, 2351, 629, 629, 2933, 2933, 1890, 1890, 593, 593, 74, 74, 1964, 1964, 2244, 2244, 1478, 1478, 496, 496, 1727, 1727, 2467, 2467, 172, 172, 2196, 2196, 465, 465, 122, 122, 141, 141, 1782, 1782, 1904, 1904, 1779, 1779, 2656, 2656, 2101, 2101, 551, 551, 1463, 1463, 311, 311, 2318, 2318, 661, 661, 213, 213, 901, 901, 1982, 1982, 1389, 1389, 68, 68, 3303, 3303, 2198, 2198, 253, 253, 464, 464, 1823, 1823, 554, 554, 406, 406, 217, 217, 715, 715, 1012, 1012, 3295, 3295, 1633, 1633, 2361, 2361, 3137, 3137, 3113, 3113]
solve(r)
print('-' * 68)
print("Test solution:")
#r = [1] * 256
isitme(r)

def sanitize(user_string):
    # user_string = str(user_string).strip('\n')
    print(user_string)
    chars = string.digits + ' ,[]'
    chars = chars.encode()
    if all(i in chars for i in user_string):
        return list(eval(user_string))

    print(b"\nNah, this is mathematical challenge\n")
    return False

def handle():
    user_input = b'[1234567]'

    my_array = sanitize(user_input)
    print(my_array)
    my_array = [1] * 256
    if my_array:
        if isitme(my_array):
            my_input = ''.join(list(map(chr, my_array)))
            print(my_input)
            if great_poem == my_input:
                print(b"\nyay, it is me: {}".format(FLAG))
            else:
                print(b'\nYou are not me!!!\n')
        
    print(b'\nTake your time and think about the input\n')

#handle()
