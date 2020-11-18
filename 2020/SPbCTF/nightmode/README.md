# Night Mode (355 pt)

Task by Dmitry Tatarov (@kukuxumushi) · Par time: ~30 min
○●●○○●●○○○○●●○●○○○○○○●○○○●○○○○○○○○○○○○○○○●○○○○○○●○○○○●○○○○●○○○○○●○●○○●●○●○○○○○○○○○○

Our developers wanted to improve their performance at night. To do this, they found a browser extension somewhere on the Internet that changes the background color, but somehow it doesn't work.

Can you help them figure it out? Hope it doesn't do anything malicious!

[nightmode.zip](nightmode.crx)

# Solution

We are given a Chrome extension, use 7zip to extract it and we see the contents.

There is malicious code inside [background.js](background.js). The code basically works as follow:
- Retrieves IP address from [https://dns.google.com/resolve?name=doyouwannaseestudentmagic.space](https://dns.google.com/resolve?name=doyouwannaseestudentmagic.space), which resolves to `64.227.77.243`
- Gets AES encryption key from [http://64.227.77.243:5000/get_aes_key](http://64.227.77.243:5000/get_aes_key): `2F423F4528482B4D6251655468566D59`
- Steals the cookie from the browser (not yet implemented in the scope of the challenge)
- Obfuscates the cookie using a custom (reversible) algorithm
- Encrypts the obfuscated cookie using AES with the key retrieved above
- Sends the cookie to [http://64.227.77.243:5000/put_cookie](http://64.227.77.243:5000/put_cookie)

To solve this challenge, first we need to get back the encrypted cookie. With some educated guess, the cookie can be retrieved at: [http://64.227.77.243:5000/get_cookie](http://64.227.77.243:5000/get_cookie)

```
JQb6BcUCAScl8x1FxQQ2WJwQNsIDAjYnJQyA+YYHFfCGT4C9JYUV3pye+pCcBO4OJQb6BcUCHSclSzbtxQQiWJxPNsacAjYnJQwd+YYHFc4lQQG9xfwV3pwP+pCcBO4OJQb6BeQCHYSGDCLtwQQ2WNYGNhPpAiInJQwdFiWaFeIlEB29JQIV3pw7+pCcBB0O
```

Then all we have to do is decrypt and deobfuscate it to retrieve the flag. Decryption is straightforward with the given `AES_Decrypt` function. I won't go into details the deobfuscation algorithm, instead I have put debugging code inside the solver for you to understand how obfuscation and deobfuscation work: [background_sol.js](background_sol.js)

```javascript
function decrypt(encrypted_cookie) {
	console.log("===== Decrypting =====");
	encrypted_cookie = atob(encrypted_cookie).split('').map(x=>x.charCodeAt(0));
	console.log("[+] Encrypted cookie array: " + encrypted_cookie);
	AES_Init();
	var decrypted_cookie = "";
	AES_ExpandKey(key);
	for (var i = 0; i < encrypted_cookie.length; i+=16) {
		var block = new Array(16);
		block = encrypted_cookie.slice(i, i + 16); 
		AES_Decrypt(block, key);
		decrypted_cookie+= String.fromCharCode.apply(null, block);
	}
	console.log("[+] AES Decrypted: " + decrypted_cookie);
	deobfuscate(decrypted_cookie);
}
```

Flag: `spbctf{JS_1s_7ra5h_0r_mag1c?}`
