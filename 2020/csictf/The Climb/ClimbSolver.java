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