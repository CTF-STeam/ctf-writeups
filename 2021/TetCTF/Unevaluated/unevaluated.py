from collections import namedtuple
from Crypto.Util.number import getPrime, isPrime, getRandomRange

Complex = namedtuple("Complex", ["re", "im"])


def complex_mult(c1, c2, modulus):
    return Complex(
        (c1.re * c2.re - c1.im * c2.im) % modulus,  # real part
        (c1.re * c2.im + c1.im * c2.re) % modulus,  # image part
    )


def complex_pow(c, exp, modulus):
    result = Complex(1, 0)
    while exp > 0:
        if exp & 1:
            result = complex_mult(result, c, modulus)
        c = complex_mult(c, c, modulus)
        exp >>= 1
    return result


class ComplexDiffieHellman:
    @staticmethod
    def generate_params(prime_length):
        # Warning: this may take some time :)
        while True:
            p = getPrime(prime_length)
            if p % 4 == 3:
                if p % 3 == 2:
                    q = (p - 1) // 2
                    r = (p + 1) // 12
                    if isPrime(q) and isPrime(r):
                        break
                else:
                    q = (p - 1) // 6
                    r = (p + 1) // 4
                    if isPrime(q) and isPrime(r):
                        break
        n = p ** 2
        order = p * q * r
        while True:
            re = getRandomRange(1, n)
            im = getRandomRange(1, n)
            g = complex_pow(Complex(re, im), 24, n)
            if (
                    complex_pow(g, order, n) == Complex(1, 0)
                    and complex_pow(g, order // p, n) != Complex(1, 0)
                    and complex_pow(g, order // q, n) != Complex(1, 0)
                    and complex_pow(g, order // r, n) != Complex(1, 0)
            ):
                return g, order, n

    def __init__(self, params=None, prime_length=128, debug=False):
        if not debug:
            raise Exception("security unevaluated")
        if params is None:
            params = ComplexDiffieHellman.generate_params(prime_length)
        self.g, self.order, self.n = params

    def get_public_key(self, private_key):
        return complex_pow(self.g, private_key, self.n)

    def get_shared_secret(self, private_key, other_public_key):
        return complex_pow(other_public_key, private_key, self.n)


def main():
    from os import urandom
    private_key = urandom(32)
    k = int.from_bytes(private_key, "big")

    cdh = ComplexDiffieHellman(debug=True)
    print("g =", cdh.g)
    print("order =", cdh.order)
    print("n =", cdh.n)
    print("public_key =", cdh.get_public_key(k))

    # Solve the discrete logarithm problem if you want the flag :)
    from secret import flag
    from Crypto.Cipher import AES
    if len(flag) % 16 != 0:
        flag += b"\x00" * (16 - len(flag) % 16)
    print("encrypted_flag = ",
          AES.new(private_key, AES.MODE_ECB).encrypt(flag))


if __name__ == "__main__":
    main()

# Output:
# g = Complex(re=20878314020629522511110696411629430299663617500650083274468525283663940214962,
#             im=16739915489749335460111660035712237713219278122190661324570170645550234520364)
# order = 364822540633315669941067187619936391080373745485429146147669403317263780363306505857156064209602926535333071909491
# n = 42481052689091692859661163257336968116308378645346086679008747728668973847769
# public_key = Complex(re=11048898386036746197306883207419421777457078734258168057000593553461884996107,
#                      im=34230477038891719323025391618998268890391645779869016241994899690290519616973)
# encrypted_flag = b'\'{\xda\xec\xe9\xa4\xc1b\x96\x9a\x8b\x92\x85\xb6&p\xe6W\x8axC)\xa7\x0f(N\xa1\x0b\x05\x19@<T>L9!\xb7\x9e3\xbc\x99\xf0\x8f\xb3\xacZ:\xb3\x1c\xb9\xb7;\xc7\x8a:\xb7\x10\xbd\x07"\xad\xc5\x84'
