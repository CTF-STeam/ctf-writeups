# zer0pts CTF 2021

This is a good CTF with some interesting and original crypto challs, which can be solved by applying relevant crypto knowledge. Unlike some other bad one with guessy/read-the-paper challs or require advanced knowledge that you can't grasp in just a few days.

Below are writeups for some of the challs we solved during this CTF.

---
# war(sa)mup (Web - 102 pts)

This is Franklin-Reiter related message attack - [task.py](warsamup/task.py)
```python
c1 = pow(m, e, n)
c2 = pow(m // 2, e, n)
```

There are many examples on the Internet, pick one and modify it to get the problem solved. We use the following polynomials:
```python
f = (2 * m + 1) ** e - c1
g = m ** e - c2
```

Solver code: [task_solve.sage](warsamup/task_solve.sage)

Flag: `zer0pts{y0u_g07_47_13457_0v3r_1_p0in7}`

---
# OT or NOT OT (Crypto - 116 pts)

We are given the following code - [server.py](ot_or_not_ot/server.py):
```python
p = getStrongPrime(1024)

key = os.urandom(32)
iv = os.urandom(AES.block_size)
aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
c = aes.encrypt(pad(flag, AES.block_size))

key = bytes_to_long(key)
print("Encrypted flag: {}".format(b64encode(iv + c).decode()))
print("p = {}".format(p))
print("key.bit_length() = {}".format(key.bit_length()))

signal.alarm(600)
while key > 0:
    r = random.randint(2, p-1)
    s = random.randint(2, p-1)
    t = random.randint(2, p-1)
    print("t = {}".format(t))

    a = int(input("a = ")) % p
    b = int(input("b = ")) % p
    c = int(input("c = ")) % p
    d = int(input("d = ")) % p
    assert all([a > 1 , b > 1 , c > 1 , d > 1])
    assert len(set([a,b,c,d])) == 4

    u = pow(a, r, p) * pow(c, s, p) % p
    v = pow(b, r, p) * pow(c, s, p) % p
    x = u ^ (key & 1)
    y = v ^ ((key >> 1) & 1)
    z = pow(d, r, p) * pow(t, s, p) % p

    key = key >> 2

    print("x = {}".format(x))
    print("y = {}".format(y))
    print("z = {}".format(z))
```

Here's how it works:
- The goal is to recover the key bits by bits, and use it to decrypt the flag.
- For each 2 bits of the key, we need to control the inputs (`a`, `b`, `c`, `d`) somehow to extract the bits from the outputs (`t`, `x`, `y`, `z`).
- A check is in place (`a`, `b`, `c`, `d` must be greater than 1) to make sure it cannot be solved the easy/trivial way.

Here's how we solved it:
- Set `a` to `2`
- Set `b` to `a * (p - 1) % p`
- Set `c` to `inverse(t, p)`
- Set `d` to `inverse(a, p)`

We recover the first bit by checking the value of `xz = x * z % p`:
- If key bit is `0`: `x = u` => `xz = (pow(a, r, p) * pow(c, s, p) % p) * (pow(d, r, p) * pow(t, s, p) % p) % p = pow(a * d, r, p) * pow(c * t, r, p) % p = 1`

We recover the second bit by checking the value of `yz = y * z % p`:
- If key bit is `0`: `y = v` => `yz = (pow(b, r, p) * pow(c, s, p) % p) * (pow(d, r, p) * pow(t, s, p) % p) % p = pow(b * d, r, p) * pow(c * t, r, p) % p`, which is `1` (if `r` is even) or `p - 1` (if `r` is odd)

Solver code: [ot_sol.py](ot_or_not_ot/ot_sol.py)

Program output:
```
a = 2
b = 132907220185736285897991772281464695170987101316907281786501076541775189926811683346224427234310580823608429105406137831547155548786641633486868555632551195792848008460529033215706439734358461222539357850771879859169086946173463939114384038750454771945402410091580923088231779749755644631041039304050302267945
c = 61032772421783423831425911203481998990741341779791222862563220424445131302911743775917373105917434434615793568321525364115721260158967046924990245293008637454180239616672227809997797938562289505238854629221751274000888900272873691116281078754328975560245629453423121175361719064758183248134452949551717042910
d = 66453610092868142948995886140732347585493550658453640893250538270887594963405841673112213617155290411804214552703068915773577774393320816743434277816275597896424004230264516607853219867179230611269678925385939929584543473086731969557192019375227385972701205045790461544115889874877822315520519652025151133974
x = 108564371397438402689353269639067770166882237942831548939762890235937330611799535874509992388440807229435015988300337795339983521508809181320127347291879039731041643540408111625442292800610421746206254219910945528869839005738606569250916613687497483229613568731318914865932834218472920054681357591353835620308
y = 108564371397438402689353269639067770166882237942831548939762890235937330611799535874509992388440807229435015988300337795339983521508809181320127347291879039731041643540408111625442292800610421746206254219910945528869839005738606569250916613687497483229613568731318914865932834218472920054681357591353835620309
z = 69474036712739164851011622982969948038792452444794860004013482853532206107824752745807346735230068109744401982580352429444507208221878812701682124298848978724693802427868180016642062952370940849088669335354915263635707509744631902748940253477249580124160929084541865032361420999706960022420775998151720509927
Key: 0101001101011011011010111101000011111010111011001101100011010000111010010111100000110011111110100001110101111010110010100100100000000110011100101011010100000011110000000111001111000101111111101110001011110111010111111001010100111100110101110010011110101110
IV: b'T1VknRdq4FSMFpp6oDgfbg=='
Ciphertext: b'MhrolctEj18YjX+31UfU21YO2CU7cajwBf/2q7dtK+0='
[*] Switching to interactive mode
[*] Got EOF while reading in interactive
```

AES decryption is not included in the code (in order to not waste time on coding mistake :P). You can use CyberChef to decrypt it. Flag: `zer0pts{H41131uj4h_H41131uj4h}`
