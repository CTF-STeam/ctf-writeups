import zlib

crc = hex(zlib.crc32(b'IHDR\x00\x00\x01\x5E\x00\x00\x00\x96\x08\x06\x00\x00\x00') & 0xffffffff)

print(crc)

for x in range(0,5):
    for y in range(0,5):
        for z in range(0,256):
            for t in range(0,256):
                crc = zlib.crc32(b'IHDR\x00\x00' + chr(x) + chr(z) + b'\x00\x00' + chr(y) + chr(t) + b'\x08\x06\x00\x00\x00') & 0xffffffff
                if crc == 0x56250434L:
                    print(hex(x), hex(z), hex(y), hex(t), hex(crc))

#0x1
#0x0
#0xa4
#0x45
