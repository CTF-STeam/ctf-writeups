# Google CTF 2025 – `crypto_numerology` (Crypto, 50 pts)

> *“I made a new cipher, can you help me test it? I'll give you the key, please use it to decrypt my ciphertext.”*

Writeup by [STeam](https://ctftime.org/team/681). Follow our [Facebook](https://www.facebook.com/steam.ctf) for more interesting security-related stuff

---
## Challenge Summary

We were given a custom stream cipher, a known key, a fixed plaintext, many ciphertext pairs with known nonces and counters, and a target ciphertext (the flag) encrypted under unknown nonce/counter. The goal was to decrypt the flag.

---
## Files Provided

- `crypto_numerology.py`: The cipher implementation
- `ctf_challenge_package.json`: JSON dataset of known plaintext/ciphertext pairs, together with the key and encrypted flag
- `init.sh`: Challenge generation script
- `flag.txt`: Sample flag
- `readme.md`: Brief description

---
## 1. Cipher Internals

The cipher in `crypto_numerology.py` is based on [ChaCha20](https://cr.yp.to/chacha.html), but heavily modified:

- It allows **1 to 8 single-round operations** (not 20 double-rounds like real ChaCha20).
- Each round applies one quarter-round function from a static list of 8.
- It uses a fixed set of constants (`CHACHA_CONSTANTS`) in state setup.
- Like ChaCha20, the output keystream is generated from a 512-bit (64-byte) block.

### `make_block(...)`

The keystream is generated via this function:

```python
def make_block(key_bytes, nonce_bytes, counter_int, constants, rounds=8)
```
**Steps to generate one `keystream_block`:**

1.  **Initialize state** as a 16-word array:
```python
state[0..4]   = constants
state[4..12]  = 256-bit key split into 8 words
state[12]     = counter (32-bit)
state[13..16] = 96-bit nonce split into 3 words
```
2.  **Save the initial state.**

3.  **Apply up to 8 single quarter-rounds** (from a list) based on `rounds` value:
```python
qr_operations_sequence = [
    lambda s: mix_bits(s, 0, 4, 8, 12),
    lambda s: mix_bits(s, 1, 5, 9, 13),
    ...
]
```
4.  **Add the original state back to the modified state**.

5.  **Convert the state into bytes** and return it.

The resulting 64-byte block is XOR-ed with the message bytes to encrypt or decrypt.

---
## 2. Known Plaintext-Ciphertext Analysis

The challenge gave us ~60 plaintext/ciphertext pairs using the same key and plaintext but different counters and nonces (`000010...`, `000020...`).

This gave us insight into how the keystream evolves with counter changes.

---
## 3. Solving Strategy

The flag ciphertext was given in `ctf_challenge_package.json`. We were given:

-   The **key** is known.
-   The **nonce** used for the flag could be one of the many seen in training.
-   The **counter** is unknown.

### 🔑 Trick

The `get_bytes` function could also be used for decryption.

Just by using a sample **nonce = `000010000000000000000000`** and a random counter `1`, we could recover more than a half of the flag.

We brute-forced the **counter** by regenerating keystream blocks for increasing values, and XOR-ing them against the flag ciphertext until we found a meaningful ASCII string starting with `CTF{`.

---
## 4. Flag

After brute-forcing the correct counter value (with fixed key and nonce), we obtained:

```
CTF{w3_aRe_g0Nn@_ge7_MY_FuncKee_monkey_!!}
```
✅

----------
## 5. Key Points

-   The cipher is ChaCha-like, but weak due to:
    -   Very few rounds (only 1 round used in the challenge).
    -   Entire keystream block predictable and brute-forceable.
-   Known-plaintext keystream recovery made it easy to test candidate counter values.
-   Only 96-bit nonces and 32-bit counters — practical to brute-force if reduced rounds are used.

----------
## Difficulty
⭐☆☆☆☆ (Easy)

----------
## Takeaways

-   Modified ciphers often introduce weaknesses even if based on strong primitives.
-   Stream ciphers + known plaintext = keystream recovery.
-   With known key and enough samples, brute-forcing a 32-bit counter is very feasible.
