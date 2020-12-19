#python3
from hashlib import md5
from binascii import unhexlify
from os import system

def padding(text):
    pad = ('\x30'*(64 - (len(text) % 64))).encode()
    return pad+text

def get_block(intro):
    unhex = unhexlify(str(input(intro)))
    return (padding(unhex))

cmd = get_block('Type your command here: ')
recmd = get_block('Retype your command here: ')

check1 = md5(cmd).hexdigest()
check2 = md5(recmd).hexdigest()

#Sector1
checkpoint=0
for i in range(len(cmd)):
    if cmd[i:i+3] == b'DTU':
        checkpoint=i
        break
    else:
        checkpoint=0

#Sector2 (Remember only 'ls' and 'cat' are allowed)
if len(cmd) == len(recmd) and cmd != recmd and check1 == check2:
    if checkpoint == 0:
        print ('Wrong checkpoint')
    elif cmd[:checkpoint] == cmd[-checkpoint:]:
        output = system(cmd[:checkpoint])
        print (output)
else:
    print ('''Nope! You're not a Magician, Dude5.''')
