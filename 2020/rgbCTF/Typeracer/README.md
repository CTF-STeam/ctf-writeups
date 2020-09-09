The minified code looks crazy. However there is a web site that makes understanding the code much easier: [http://www.jsnice.org/](http://www.jsnice.org/)

The interesting part is here:

```
"_0x1c2030" : _0x7379("0x20", "zyUu") + "ou have be" + _0x7379("0x4c4", "9f2)") + _0x7379("0x570", "Y@$M") + _0x7379("0x505", "XVoV") + "iQ1RGe3c0M" + _0x7379("0x649", "*a95") + _0x7379("0x55a", "nB&s") + "l80bm4weTF" + _0x7379("0x143", "&H2q"),
```

Which corresponding to the following part:

```
'\x5f\x30\x78\x31\x63\x32\x30\x33\x30': _0x7379('\x30\x78\x32\x30', '\x7a\x79\x55\x75') + '\x6f\x75\x20\x68\x61\x76\x65\x20\x62\x65' + _0x7379('\x30\x78\x34\x63\x34', '\x39\x66\x32\x29') + _0x7379('\x30\x78\x35\x37\x30', '\x59\x40\x24\x4d') + _0x7379('\x30\x78\x35\x30\x35', '\x58\x56\x6f\x56') + '\x69\x51\x31\x52\x47\x65\x33\x63\x30\x4d' + _0x7379('\x30\x78\x36\x34\x39', '\x2a\x61\x39\x35') + _0x7379('\x30\x78\x35\x35\x61', '\x6e\x42\x26\x73') + '\x6c\x38\x30\x62\x6d\x34\x77\x65\x54\x46' + _0x7379('\x30\x78\x31\x34\x33', '\x26\x48\x32\x71'),
```

Running this on Google Chrome console and we'll get the flag:

```
"Congrats you have beaten me! Here's your flag: cmdiQ1RGe3c0MHdfajR2NDJjcjFwN18xMl80bm4weTFuZ30="
```

Flag: `rgbCTF{w40w_j4v42cr1p7_12_4nn0y1ng}`
