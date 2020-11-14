# Magically Delicious (100 pt)

Can you help me decipher this message?

⭐🌈🍀 ⭐🌈🦄 ⭐🦄🌈 ⭐🎈🍀 ⭐🦄🌑 ⭐🌈🦄 ⭐🌑🍀 ⭐🦄🍀 ⭐🎈⭐ 🦄🦄 ⭐🦄🎈 ⭐🌑🍀 ⭐🌈🌑 ⭐🌑⭐ ⭐🦄🌑 🦄🦄 ⭐🌑🦄 ⭐🦄🌈 ⭐🌑🍀 ⭐🦄🎈 ⭐🌑🌑 ⭐🦄⭐ ⭐🦄🌈 ⭐🌑🎈 🦄🦄 ⭐🦄⭐ ⭐🌈🍀 🦄🦄 ⭐🌈🌑 ⭐🦄💜 ⭐🌑🦄 🦄🦄 ⭐🌑🐴 ⭐🌑🦄 ⭐🌈🍀 ⭐🌈🌑 🦄🦄 ⭐🌑🦄 ⭐🦄🌈 ⭐🌑🍀 ⭐🦄🎈 ⭐🌑🌑 ⭐🦄⭐ ⭐🦄🌈 ⭐🌑🎈 🦄🦄 ⭐🦄🦄 ⭐🌑🦄 ⭐🌈🌑 ⭐🦄💜 ⭐🦄🎈 ⭐🌑🌑 ⭐🎈🦄

Note: If you don't see a message above, make sure your browser can render emojis.

Tip: If you're digging into the unicode encoding of the emojis, you're on the wrong track!

Author: meowmeow (not on Discord, message kcolley any questions)

# Solution

Although many people think this crypto challenge is terrible, I myself think it's quite good - solvable with cryptanalysis.

Observation of the ciphertext:
- Consists of 8 different emojis, in which 💜 and 🐴 appear at low frequency
- Emojis come in groups of 3, separated by whitespaces. An exceptional case is 🦄🦄
Now we can assume that substitution cipher is used. Each group of 3 emojis stands for 1 character. 🦄🦄 is probably separator.

Let's try replacing each group of emojis with a different character, 🦄🦄 with underscore:

```
abcdebfgh_ifjke_lcfimnco_na_jpl_qlaj_lcfimnco_rljpims
```

Looks like the plaintext is a flag without anything else, let's try fitting it in flag format:

```
abcdebfgh_ifjke_lcfimnco_na_jpl_qlaj_lcfimnco_rljpims
sun{?u???_?????_?n????n?_?s_???_??s?_?n????n?_??????}
```

Best candidate for `?s` is `is`:

```
abcdebfgh_ifjke_lcfimnco_na_jpl_qlaj_lcfimnco_rljpims
sun{?u???_?????_?n???in?_is_???_??s?_?n???in?_??????}
```

Now we use [onelook](https://www.onelook.com/?w=?n???in?&ssbp=1&scwo=1&sswo=1) to search for words with `?n???in?` pattern. `anything`, `enjoying` and `encoding` seem to be the most suitable options, among which `encoding` gives the best decryption:

```
abcdebfgh_ifjke_lcfimnco_na_jpl_qlaj_lcfimnco_rljpims
sun{?uc??_oc???_encoding_is_??e_?es?_encoding_?e??od}
```

Something about the best encoding method, let's see what we have here:

```
abcdebfgh_ifjke_lcfimnco_na_jpl_qlaj_lcfimnco_rljpims
sun{?uc??_oct??_encoding_is_the_best_encoding_method}
```

From here we can see that octal is used and use that knowledge to find the correlation between the emojis and octal digits.

```
⭐ = 1  🌈 = 6  🍀 = 3  🦄 = 5  🎈 = 7  🌑 = 4  🐴 = 2  💜 = 0
```

Now time to convert from octal to ascii and get the flag:

```
163 165 156 173 154 165 143 153 171 55 157 143 164 141 154 55 145 156 143 157 144 151 156 147 55 151 163 55 164 150 145 55 142 145 163 164 55 145 156 143 157 144 151 156 147 55 155 145 164 150 157 144 175
sun{lucky-octal-encoding-is-the-best-encoding-method}
```
