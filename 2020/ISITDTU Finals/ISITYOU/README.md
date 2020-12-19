We are given the server code in [](isityou.py), the following part is important:

```
FLAG = open('flag.txt','rb').read()
great_poem = open('my_poem.txt').read()

# What the heck?
WTF = ord('c')*11
WTF += ord('o')*9
WTF += ord('t')*5
WTF += ord('h')*3
WTF += ord('A')*2
WTF += ord('n')*2


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

    c = 1
    for o in range(7, 0, -1):
        t = 1 << o
        for h in range(0, 256, 1 << (o+1)):
            a = _a[c]
            for n in range(h, t+h, 2):
                co = n + t
                th = n

                an = (a * r[co]) % (WTF - 1)
                r[co] = (r[th] - an) % (WTF - 1)
                r[th] = (r[th] + an) % (WTF - 1)

            c += 1

    c = 1
    for o in range(7, 0, -1):
        t = 1 << o
        for h in range(1, 256, 1 << (o+1)):
            a = _a[c]
            for n in range(h, t+h, 2):
                co = n + t
                th = n

                an = (a * r[co]) % (WTF - 1)
                r[co] = (r[th] - an) % (WTF - 1)
                r[th] = (r[th] + an) % (WTF - 1)
            c += 1

    return True
...
    def handle(self):
        self.request.settimeout(30)
        rsend = self.request.sendall
        rclose = self.request.close
        rrecv = self.request.recv

        rsend(Welcome)

        rsend(b'\nIs it You?\n> ')
        user_input = rrecv(4096).strip()

        my_array = self.sanitize(user_input)
        print(my_array)
        if my_array:
            if isitme(my_array):
                my_input = ''.join(list(map(chr, my_array)))
                if great_poem == my_input:
                    rsend(b"\nyay, it is me: {}".format(FLAG))
                else:
                    rsend(b'\nYou are not me!!!\n')
...
```

The code is completely reversable, although it is quite tricky, you have to reverse in the right order to get the solution.

I'm busy so you should inspect the (a bit messy) solver code yourself: [isityou_solve.py](isityou_solve.py)

Flag:

```
nc 34.123.55.74 25537
Welcome to self-identification service.
This is the place only me-myself-I can get in. Come on, go on, fsk me!!!

Is it You?
> [1306, 2733, 154, 1653, 2270, 1771, 1841, 1340, 2713, 2398, 885, 675, 1588, 819, 1253, 2654, 1491, 2997, 601, 425, 1522, 1172, 2412, 1643, 3265, 1696, 0, 565, 301, 1911, 1359, 280, 3315, 396, 269, 185, 1918, 1249, 3166, 910, 715, 1559, 2455, 382, 1548, 1455, 3193, 1918, 3062, 1489, 1473, 772, 2784, 1716, 2795, 3327, 3172, 216, 2072, 3014, 1607, 3126, 126, 1509, 2619, 2317, 1525, 182, 281, 2982, 1097, 3295, 3285, 1761, 2482, 709, 2144, 1183, 2680, 154, 1530, 2633, 1804, 663, 1025, 756, 1998, 945, 1318, 3309, 1721, 431, 860, 2836, 2279, 1509, 3200, 498, 266, 2350, 233, 1490, 2699, 3073, 1806, 2035, 1946, 237, 1105, 2069, 541, 3030, 3115, 1293, 1440, 2735, 2056, 138, 3298, 2699, 3126, 597, 268, 1826, 827, 2714, 2453, 3190, 375, 3170, 3221, 997, 2318, 906, 1131, 2468, 477, 2686, 700, 853, 2007, 2121, 595, 226, 1731, 2048, 671, 2986, 1806, 2317, 2988, 1988, 2928, 999, 1092, 1305, 874, 2886, 2854, 2035, 318, 2614, 911, 875, 679, 1512, 2043, 2736, 813, 337, 3010, 1522, 2680, 1115, 134, 1942, 1103, 1081, 894, 2788, 1736, 303, 1914, 903, 1190, 967, 2102, 2453, 583, 1825, 1014, 2038, 563, 2983, 0, 883, 882, 516, 1303, 568, 3060, 1780, 46, 1952, 916, 1059, 1863, 643, 1111, 2061, 2191, 2992, 2075, 2215, 2452, 3116, 1091, 2866, 1571, 2688, 1502, 1825, 2315, 216, 1360, 2132, 2189, 808, 22, 1377, 951, 2117, 2622, 1396, 1229, 485, 183, 1818, 560, 825, 2525, 3208, 2783, 1517, 690, 1774, 1535, 419, 796, 720, 982, 3015, 2044, 1520, 1734, 1632]
yay, it is me: b'ISITDTU{W0w_Numb3r_ThEor3t1c_tr4nsf0rm_1S_c00l!}\n'
Take your time and think about the input
```

(The redundant "Take your time and think about the input" is probably a bug in the code, it doesn't really matter :P)
