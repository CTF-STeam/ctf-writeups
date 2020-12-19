#!/usr/bin/env python3
import os
from hashlib import sha256
from random import randint
import string
import threading
import socketserver
import string

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


Welcome = b"""Welcome to self-identification service.
This is the place only me-myself-I can get in. Come on, go on, fsk me!!!
"""


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def sanitize(self, user_string):
        # user_string = str(user_string).strip('\n')
        print(user_string)
        chars = string.digits + ' ,[]'
        chars = chars.encode()
        if all(i in chars for i in user_string):
            return list(eval(user_string))

        self.request.send(b"\nNah, this is mathematical challenge\n")
        return False

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
            
        rsend(b'\nTake your time and think about the input\n')
        rclose()

HOST, PORT = "localhost", 25537

server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

# Start a thread with the server -- that thread will then start one
# more thread for each request
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread:", server_thread.name)
server_thread.join()

# Go on, brutEEEEEEEEEEEEEEEEEEEEEEEEEee!!!!
