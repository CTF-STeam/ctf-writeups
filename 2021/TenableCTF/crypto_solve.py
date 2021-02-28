

def xor(a, b):
    x = [None] * len(a)
    for i in range(len(a)):
        if i < len(b):
            x[i] = a[i] ^ b[i]
        else:
            x[i] = a[i]
    return bytes(x)

def rev(a):
    return a[::-1]

trx = b'GED\x03hG\x15&Ka =;\x0c\x1a31o*5M'
drx = b"LemonS"
trx = xor(trx, drx)
drx = b"caviar"
drx = rev(drx)
trx = xor(trx, drx)
trx = rev(trx)
drx = b"vaniLla"
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
trx = rev(trx)
drx = b"tortillas"
trx = xor(trx, drx)
drx = b"applEs"
trx = xor(trx, drx)
drx = b"miLK"
drx = rev(drx)
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
trx = rev(trx)
trx = rev(trx)
trx = rev(trx)
drx = xor(drx, drx)
trx = xor(trx, drx)
drx = b"OaTmeAL"
trx = xor(trx, drx)
trx = rev(trx)
trx = rev(trx)
trx = rev(trx)
drx = xor(drx, drx)
trx = xor(trx, drx)
drx = b"cereal"
trx = xor(trx, drx)
drx = b"ICE"
drx = rev(drx)
trx = xor(trx, drx)
drx = b"cHerries"
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
trx = rev(trx)
drx = b"salmon"
trx = xor(trx, drx)
drx = b"chicken"
trx = xor(trx, drx)
drx = b"Grapes"
drx = rev(drx)
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
trx = rev(trx)
drx = b"caviar"
drx = rev(drx)
trx = xor(trx, drx)
trx = rev(trx)
drx = b"vaniLla"
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
drx = trx
trx = b"HonEyWheat"
drx = xor(drx, trx)
trx = drx
drx = b"HamBurgerBuns"
drx = rev(drx)
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
trx = rev(trx)
trx = rev(trx)
trx = rev(trx)
drx = xor(drx, drx)
trx = xor(trx, drx)
drx = b"IceCUBES"
trx = xor(trx, drx)
drx = b"BuTTeR"
trx = xor(trx, drx)
trx = rev(trx)
trx = xor(trx, drx)
trx = rev(trx)
drx = b"CaRoTs"
trx = xor(trx, drx)
drx = b"strawBerries"
trx = xor(trx, drx)
print(trx)

