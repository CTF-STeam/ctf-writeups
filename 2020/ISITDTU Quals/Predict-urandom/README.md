There is a bug with the code, the same 16-byte xor key is used for all blocks.

[xortool](https://github.com/hellman/xortool) can help you recover like 50% of the plaintext.

Known plaintext attack with [otp_pwn](https://github.com/derbenoo/otp_pwn) and you'll get the rest of the plaintext.
