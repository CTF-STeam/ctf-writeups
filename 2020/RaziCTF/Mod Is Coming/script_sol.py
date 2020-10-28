from numpy import array
from PIL import Image
from Crypto.Util.number import inverse

img = Image.open('enc.png')
image = array(img)
x, y, z = image.shape
s = [''] * x
for a in range (0, x):
    for b in range (0, 1):
        p = image[a, b]
        tensa = p[1] - p[0] if p[1] > p[0] else 251 - p[0] + p[1]
        s[a] = chr(tensa * inverse(10, 251) % 251)
print(''.join(s))
