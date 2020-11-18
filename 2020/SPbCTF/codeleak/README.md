# Leaked Code (213 pt)

Task by George Zaytsev (@groke) · Par time: ~30 min
○●●○○○●○○○○●●○●●●●○○○●○●○●●○○○○○●○○○○●○○○○○○●○○●●○○○○●○○○○●○○○○●○○●○●○●●●○○○○○○○○○○

During internal pentest we've been able to make a photo of security engineer's computer screen.

It seems that he is reverse engineering his employer's internal access system algorithms. Can you help us get a valid access code?

Here are your files: [codeleak_6acc7c63ac.zip](codeleak_6acc7c63ac.zip)

# Solution

Although at medium difficulty, this challenge isn't very complicated with some Java knowledge. You can study the code yourself :P

```python
alphabet = 'abcdefghijklmnopqrstuvwxyz_!@'
flag = 'spbctf{'
seed = 5
for i in range(7, 23):
    flag += alphabet[seed]
    seed = seed * 3 % len(alphabet)
flag += '}'
print(flag)
```

Flag: `spbctf{fpqt@_ucgszrwiyo}`
