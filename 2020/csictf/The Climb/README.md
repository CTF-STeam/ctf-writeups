The flag is encrypted using [Hill cipher](https://en.wikipedia.org/wiki/Hill_cipher), in which every block of 3 is multiplied by a 3x3 matrix.

The official way to solve it is by solving a system of equations (using [Gaussian elimination](https://en.wikipedia.org/wiki/Gaussian_elimination) or similar methods).

Or it can be solved by bruteforcing all trigram conbinations, which is easier to implement :P

Modification of theclimb.java to allow us to reuse the code (you need to rename it to [Main.java](Main.java) or remove the public access modifier for it to compile):
```
public String res(int len)
{
	String res = "";
	for (int i = 0; i < len; i++)
	{
		res += (char) (rmatrix[i] + 97);
	}
	//System.out.print(res);
	return res;
}
```

And here's the solver code: [ClimbSolver.java](ClimbSolver.java)
```
public class ClimbSolver {
	static String encrypted = "lrzlhhombgichae";
	static String key = "gybnqkurp";
	
	public static void brute(int startPos) {
		int size = (int) Math.sqrt(key.length());
		String encChunk = encrypted.substring(startPos, startPos + size);
		Main obj = new Main();
		obj.keyconv(key, size);
		for (char a = 'a'; a <= 'z'; a++)
		for (char b = 'a'; b <= 'z'; b++)
		for (char c = 'a'; c <= 'z'; c++) {
			String text = "" + a + b + c;
			obj.textconv(text);
			obj.multiply(text.length());
			String res = obj.res(text.length());
			if (res.equals(encChunk)) {
				System.out.print(text);
			}
		}
	}
	
    public static void main(String[] args) {
		for (int i = 0; i < encrypted.length(); i += 3) {
			brute(i);
		}
		System.out.println();
    }
}
```

Output:

```
hillshaveeyesxx
```

Flag: `csictf{hillshaveeyes}`
