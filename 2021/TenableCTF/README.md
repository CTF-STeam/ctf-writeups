# Classic Crypto (Crypto - 50 pts)

This is Vigenere cipher. From the encrypted flag `zdat{qyyegcuvvurlqfy}`, we try to decrypt with `flag{}` as known plaintext and recover the key `anonymous`.

Fully decrypted text:

```
There are many theories about us. That we’re anarchists, kids, crazy film-buffs that saw one too many superhero movies. The truth is, we are all these things. Anonymous is a symbol, like the flag a country flies. The flag is the symbol of the country. Our masks are our national identity. We are not Anonymous – we represent the ideals of Anonymous. Truth, freedom and the removal of censorship. Like any symbol, we affix it wherever we go, as you have seen from street protests.

We have no leaders, civilians or soldiers. We are all one. We run operations because that is what the group decides to do. We choose targets because that is what the people who represent the ideals of Anonymous want to fight for. The world is in trouble. We see it every day – war, poverty, murder. Every day we are bombarded with news and images, as we sit at home safe in the knowledge that we are powerless, that “better” minds are dealing with the situation.

But what if you could be the change you want to see? I’m twenty five years old. I went to school and college. I fought for my country then got a job and paid my taxes. If you met me on the street I wouldn’t even register on your radar. I am just another person in a sea of faces.

But in cyberspace we are different. We helped free the people of Egypt. We helped fight against Israel as it attempted genocide. We exposed more than fifty thousand paedophiles around the world. We fought the drug cartels. We have taken to the streets to fight for the rights you are letting slip through your fingers.

We are Anonymous.

The flag is "flag{classicvigenere}"

In today’s world we are seen as terrorists or at best dangerous anarchists. We’re called “cowards” and “posers” for hiding behind masks, but who is the real poser? We take away the face and leave only the message. Behind the mask we could be anyone, which is why we are judged by what we say and do, not who we are or what we have.

We exist without nationality, skin colour or religious bias.
```

---
# Find the encoding (Misc - 50 pts)

This is base58, use [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base58('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',true)&input=RGVabXFNVWtESmNleWNKSEpQelpldA) to decode it.

Flag: `flag{not_base64}`

---
# ECDSA Implementation (Crypto - 225 pts)

This challenge is about ECDSA nonce-reuse weakness. See [this post](https://ropnroll.co.uk/2017/05/breaking-ecdsa/) for explanation.

Solver code: [ecdsa_solve.py](ecdsa_solve.py)

Flag: `flag{cRypt0_c4r3fully}`

---
# Is the King in Check? (Coding - 200 pts)

This chall is fairly simple, it can be solved by checking for threats from enemy pieces:
- For enemy queen, rooks, bishops: check the closest piece in all horizontal, vertical and diagonal directions
- For enemy knights: check all 8 possible attacking positions
- For enemy pawns: check 2 possible attacking positions

Full solver code: [kingcheck_solve.py](kingcheck_solve.py)

(Boundary checks can be ignored, test cases do not include them. Code can be shortened further, but this was how our team solved the chall :P)
