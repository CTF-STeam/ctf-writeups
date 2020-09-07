import zlib

crc = hex(zlib.crc32(b'IHDR\x00\x00\x01\x5E\x00\x00\x00\x96\x08\x06\x00\x00\x00') & 0xffffffff)

print(crc)

for x in range(0,256):
    for y in range(0,256):
        for z in range(0,256):
            for t in range(0,256):
                crc = zlib.crc32(b'IHDR\x00\x00' + bytearray([x, z]) + b'\x00\x00' + bytearray([y, t]) + b'\x08\x06\x00\x00\x00') & 0xffffffff
                if crc == 0xe3677ec0:
                    print(hex(x))
                    print(hex(y))
                    print(hex(z))
                    print(hex(t))

#0x3
#0x1
#0x6e
#0x49
