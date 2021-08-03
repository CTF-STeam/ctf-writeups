# back_to_basics (Crypto - 50 pts)

This can easily be solved by bruteforcing each character of the key. Full code: [main_basic_solve.py](main_basic_solve.py).
```python
def all_valid(b):
    return all(x >= 32 and x < 128 for x in b)

def bf_key(flag_enc):
    for c in ALPHABET:
        try:
            flag = base_n_decode(flag_enc, ALPHABET.index(c))
            if all_valid(flag):
                    return c, flag
        except:
                continue
    return None

with open("flag_enc", "rb") as f:
    flag_enc = f.read()
print(flag_enc[:16])

key = ''
while len(flag_enc) > 16:
    c, flag_enc = bf_key(flag_enc)
    key += chr(c)
    print(key, flag_enc[:16])
```

Output:
```
b'R4OH278SS4ME1O64'
W b'6LDGG8K88173K5GH'
WM b'4141131300202234'
WM5 b'1S4UTSOJMB2C2LT3'
WM5Z b'3046215040463144'
WM5Z8 b'124A3243B2242697'
WM5Z8C b'138QP2FHMKJ71NED'
WM5Z8CR b'233BDI37C8468GBH'
WM5Z8CRJ b'6721621858612322'
WM5Z8CRJ0 b'1513A70901445151'
WM5Z8CRJ0B b'P3R7VG5G8BHAENEU'
WM5Z8CRJ0BX b'58DE8D165744E76I'
WM5Z8CRJ0BXJ b'2BCB0164601BA772'
WM5Z8CRJ0BXJD b'DCD3D7GB74EB1HFE'
WM5Z8CRJ0BXJDJ b'4023233122443204'
WM5Z8CRJ0BXJDJ5 b'ELKNAORKCPTN4D24'
WM5Z8CRJ0BXJDJ5W b'uiuctf{r4DixAL}'
```

---
# dhke_intro (Crypto - 50 pts)

Here `p` is small, and so is `k`. We [bruteforce](dhkectfintro_solve.py) all values of `k` from 0 to 30 and see which one gives us the flag.

```python
ciphertext = unhexlify('b31699d587f7daf8f6b23b30cfee0edca5d6a3594cd53e1646b9e72de6fc44fe7ad40f0ea6')

iv = bytes("kono DIO daaaaaa", encoding = 'ascii')
for k in range(31):
    key = pad_key(str(k))
    cipher = AES.new(key, AES.MODE_CFB, iv)
    flag = cipher.decrypt(ciphertext)
    if b'uiuctf' in flag:
        print(flag)
```

Flag: `uiuctf{omae_ha_mou_shindeiru_b9e5f9}`

---
# dhke_adventure (Crypto - 65 pts)

We are allowed to control DHKE's prime number `p`. It is known that if `p` is weak (`p - 1` consists of small factors), we can easily solve discrete log problem using Pohlig–Hellman algorithm.

Here's [the code](dhkeadv_primegen.py) I used to generate weak prime number:
```python
while True:
    p = 2
    while p.bit_length() < 1024:
        p *= getPrime(16)
    if p.bit_length() < 2048:
        p = p + 1
    if isPrime(p):
        print(p)
        break
    else:
        print('Failed')
```

Now use the prime generated to [break the key exchange and recover the flag](dhkeadv_solve.sage):
```python
from binascii import unhexlify
from Crypto.Cipher import AES
from hashlib import sha256

p = 13235062921662694429211184891220141973285969028958016790661658609292023032453887458389574420664371217218833375173082540739555090686687826551693380798574629365254210787419070348340076227508521415632755789594367616391764583712987637766374230688082101873347891400341145784790200266806419168972691757367828474132879
g = 2

# dio = pow(g,a,p)
dio = 3792084934906248564383234181650035598772615324676195889910857921102049947444713668894077270359500041848160892283875666632138773227678174413239166356643157564701755290320942846789533398104751824380490988637885367504561459997920826443858290627891230160540485823054473058723700613322991694411069864630317229002911
# jotaro = pow(g,b,p)
jotaro = 1264790617152365852095129131541764881757215378660064894337475150769922800524031374528216985077846999998895522436779903552749896067733534664389692778794818553787963498827277500298297339946818247400174112120794559981652711640384257027450857601018904217492079212562792889181540706049350288847341968603810689566739

ct = 'a7a7cb1f26d3d2770f82d5fb45710ed4519ba04dd7ec5950ba8f2b4a9e013a194b265ba3233e5d288702'
ct = unhexlify(ct)

F = IntegerModRing(p)

a = discrete_log(F(dio), F(g))
print(a)

key = pow(jotaro, a, p)
key = sha256(str(key).encode()).digest()

iv = b'uiuctf2021uiuctf'
cipher = AES.new(key, AES.MODE_CFB, iv)
pt = cipher.decrypt(ct)
print(pt)
```

Flag: `uiuctf{give_me_chocolate_every_day_7b8b06}`
