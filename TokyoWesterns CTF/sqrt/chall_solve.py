from Crypto.Util.number import bytes_to_long, isPrime, long_to_bytes, inverse

ct = 5602276430032875007249509644314357293319755912603737631044802989314683039473469151600643674831915676677562504743413434940280819915470852112137937963496770923674944514657123370759858913638782767380945111493317828235741160391407042689991007589804877919105123960837253705596164618906554015382923343311865102111160
p = 6722156186149423473586056936189163112345526308304739592548269432948561498704906497631759731744824085311511299618196491816929603296108414569727189748975204102209646335725406551943711581704258725226874414399572244863268492324353927787818836752142254189928999592648333789131233670456465647924867060170327150559233
print(p % 8)

def encrypt(m, k, p):
    return pow(m, 1 << k, p)

count = 0
k = 64
e = 1 << k
phi = p - 1
d = inverse(e, phi)
pt = pow(ct, d, p)

#print(e * d % phi)
#print(long_to_bytes(pt))

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)
 
def tonelli(n, p):
    #assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def print_result(pt):
    print(pt)
    with open("result.txt", "a+") as f:
        f.write(str(pt) + "\n")


def solve(n, p, k):
    global count
#    if k == 63:
#        print(n)
    if k == 0:
        #print(n)
        count += 1
        if count % 100 == 0:
            print(count)
        pt = long_to_bytes(n)
        if pt.startswith(b"TWCTF{"):
            print_result(pt)
        return
    r = tonelli(n, p)
    #if k== 64 and legendre(r, p) == 1:
    #    print(r)
    #if k== 64 and legendre(p - r, p) == 1:
    #    print(p - r)
    if k < 30 and legendre(r, p) == 1:
        solve(r, p, k - 1)
    if k < 31 and legendre(p - r, p) == 1:
        solve(p - r, p, k - 1)

solve(pt, p, 30)
#solve(ct, p, 64)
'''
n = 549612572601900444027468582786457379013683500909588206003863166767807497919403145039527369114279266051940762441956503980651245874906407074482267572796005595996944023065067438912749107687542322588916163498301331742260434244855700897782958763481662966862444418961420020159982425993594046628403442168440629575284
n = 1948865039294009691576181380771672389220382961994854292305692557649261763833149884145614983319207887860531232498119502026176334583810204964826290882842308810728384018930976243008464049012096415817825074466275128141940107121005470692979995184344972514864128534992403176506223940852066206954491827309484962494271
assert encrypt(n, k, p) == ct
print(encrypt(n, k, p))
'''
'''
flag = 'TWCTF{test}'
m = bytes_to_long(flag.encode())
ct = pow(m, 2, p)
print(ct)
solve(ct, p, 1)
'''


'''
m ^ (2^64) = xp + ct


assert flag.startswith("TWCTF{")
assert len(flag) == 42
assert isPrime(p)

pt = bytes_to_long(flag.encode())
ct = encrypt(pt, k, p)

with open("output.txt", "w") as f:
    f.write(str(ct) + "\n")
    f.write(str(p) + "\n")
'''

