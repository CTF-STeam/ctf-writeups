# Unimplemented (Crypto - 100 pts)

Tl;dr:
- This is RSA in the field of Gaussian integers, similar to a Crypto CTF 2019 challenge: [https://ctftime.org/writeup/16100](https://ctftime.org/writeup/16100)
- A paper explaining the concept with the formular for phi is here: [Modified RSA in the Domains of Gaussian Integers(https://www.semanticscholar.org/paper/Modified-RSA-in-the-Domains-of-Gaussian-Integers-El-Kassar-Haraty/4c80b6607181f06c396f91e3e385d3416adc8a63)
- Phi is calculated as: `p*p*(p*p-1)*q*q*(q*q-1)`
- Full solver code: [unimplemented_solve.py](unimplemented_solve.py)
- Flag:
```
b'}\xb0\x10\x05\x1e\xe3\xb4/\x1aoJn\xdd)\xa1Z\xe9\x0b\xee\x81,\x1e\xf7\xebp\xe2\xe0\x98\xf9\x1a\xbd5[LK\x02M\x84\xb2\xa6;D\x1e\x1a\n~Go\xb9\xbcY\x0fX=\xcd/\xb0W$\x14\xe2|\xea\xe1\x11\xda\xea\xbd\xed\xa7\x7f\xaap"\x85>\xfe\xff\xa8\xfe\x15\xd2\x8c\xe6\xeaT!&K\x1cK`z,?64\x11{U\xecM4\x15\x14\xc0\xd9\xa7\x7f\xd7\x89F\t\x8f\xf7Z;\xb6\x8f\xe6\xcc\xe9\t\x08\xd1\xac\xbb\xd8\xbb\xa3>\x99fK\xdd\xd9\x99c\xa1_\xb1091\xc5\xd6\xcc\xe4z\xd8\xb9\x0f0\xed\x15\xd9x1\xce\xcc\x99\xebu\xc4(\xfb\x88i/\xfba\xa9\x1c\x9a\xa5,j\x84<\x7f\xae\xbc\xdf.`\xff\x04\x9d#\x86B\t4\xbe\xd0\xbf!6 \x06\xa2\r1~Z\xc3\xf1\xf5\x87n\xa3\xfa\xd4\xd1\xa8\x81?\xb2#\x82\xf5\x8e\xd7\x98n\x04\xb0\xccT\xe8\xfb\xad5t\x1c\xba\x19\xea\xb7\xd4\x8d\xe0g\xb3\x94P\x8e\xe4p \x80m\x00\xba\xef=\xe9\x16\x94jd\xc01j\x8a\xd0\xad~.\xea\xad\x8c\xb0\xfc\xe4\xc5\x91\x1c\x80\xef\xdb|7\'Nh\xb8\xeb\xa8\xc2\x1aL\xc3\x14\x8a\x83\xec\xa8\xd4I\xe0\xc7\x8c\x97u\x90w\xae\xe5\x02\xa9\x9b~\x05/p\xcd\x12\xcaA/W5\xef\xd6\xa1\x85\xaf\xb2\x04\xe2O\xb9I!\xba\x1c,]o\xc3\r\xe7\x84\xa7\xad7W03w\x92\xa5\xfc\xb6\xf9\xc4\xed|\xf3\x8c\xdd\xbdrcS\x8a\xea\xab\xd0\xa1\xe6\xff\xf5F4\xb8g\xe6\x08\xf8\x899\x06\xea\x16F6\rY6\x82\xd5\x85\xaa\'Y\xb9a\x12\x95Z*y<\xfc\x9a\x9d{7G<\xe5\xc83\xa0\xca\xef\xd0,\xca\xbf\xc1Zxm\xc5\xb5\xe7\xdfq\x1e\xc1\xf5*C\x86\x1c\xcd \\Q\x10\x00TetCTF{c0unt1ng_1s_n0t_4lw4ys_34sy-vina:*100*48012023578024#}'
```
(Unpad function is broken, but I don't bother to fix it :P)
