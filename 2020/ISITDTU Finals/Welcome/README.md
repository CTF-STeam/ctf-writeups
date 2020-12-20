# Welcome (Misc - 100 pts - third blood)

We were given the following "text", and the challenge was in misc section, which told us that anything could be possible.

```
x$x%s%&LH6=4~>60E_0x$x%s%&\r%u\a~a@N
```

We suspected this was a crypto chall. Some observation of the text:
- The pattern `x$x%s%&` appeared twice
- Also, it matched the flag format `ISITDTU{}`

So it could be assumed that some kind of substitution cipher was used. We tried replacing it and figure out the rule of substitution:

```
x$x%s%&LH6=4~>60E_0x$x%s%&\r%u\a~a@N
ISITDTU{           ISITDTU  T      }
```

Looked like some kind of XOR/SHIFT was involved. Playing around with [CyberChef](https://gchq.github.io/CyberChef/), XOR gave us nothing, while SUB showed that some chars had been shifted by -47, some by +47:

```
x$x%s%&LH6=4~>60E_0x$x%s%&\r%u\a~a@N
IõIöDö÷.....O....0.IõIöDö÷-CöF-2O2..
§S§T¢TU{welc.me_t._§S§T¢TU.¡T¤....o}
```

From here we recovered the flag:

```
ISITDTU{welcOme_t0_ISITDTU-CTF-2O2o}
```

(We claimed third blood solving it this way, and only 51s slower than the first team. Later after the event ended we realized that it was just rot47)
