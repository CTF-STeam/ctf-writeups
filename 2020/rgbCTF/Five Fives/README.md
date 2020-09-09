We are given 5 random numbers generated using `SecureRandom` with `System.currentTimeMillis()` as the seed. Our task is to guess the next 5 numbers.

```
//You'll never find my seed now!
...
long seed = System.currentTimeMillis();
System.out.println(seed);
ByteBuffer bb = ByteBuffer.allocate(Long.BYTES);
bb.putLong(seed);
SecureRandom r = new SecureRandom(bb.array());
...
System.out.println("Yesterday's numbers were: ");
for (int i = 0; i != 5; i++) {
	System.out.print((r.nextInt(5) + 1) + " ");
}
...
System.out.println("You have $20, and each ticket is $1. How many tickets would you like to buy? ");
int numTries = Integer.parseInt(in.nextLine());
...
int[] nums = new int[5];
for (int a = 0; a != 5; a++) {
	nums[a] = r.nextInt(5) + 1;
	System.out.print(nums[a] + " ");
}
...
for (int i = 0; i != numTries; i++) {
	System.out.println("Ticket number " + (i + 1) + "! Enter five numbers, separated by spaces:");
	String[] ticket = in.nextLine().split(" ");
	
	boolean winner = true;
	for (int b = 0; b != 5; b++) {
		if (nums[b] != Integer.parseInt(ticket[b])) {
			winner = false;
			break;
		}
	}
	
	if (!winner) {
		System.out.println("Your ticket did not win. Try again.");
	} else {
		System.out.println("Congratulations, you win the flag lottery!");
		outputFlag();
	}
}
```

Some website says that ["SecureRandom" seeds should not be predictable](https://rules.sonarsource.com/java/tag/owasp/RSPEC-4347), so we tried to recover the seed and imitate the RNG, as in [Occasionally Tested Protocol](https://ctftime.org/task/12322). However this is practically quite hard, because `SecureRandom` also uses entropy obtained from the underlying operating system.

After some time spent trying to exploit the weakness of random seed, we switched to another approach. Because we only have to guess 5 numbers from 1 to 5, the chance of getting a correct guess is quite high (1/3125). With 20 tries, this is even higher. And even more, **there is a bug in the program that gives you a sure win**:

```
int numTries = Integer.parseInt(in.nextLine());
if (numTries > 20) {
	System.out.println("Sorry, you don't have enough money to buy all of those. :(");
	System.exit(0);
}
...
for (int i = 0; i != numTries; i++) {
...
}
```

The program only checks if your number of tries does not exceed 20, and the loop only terminates if the counter equals numTries. So if you enter a negative value, the loop will not end until you reach an overflow, which means you have (almost) **unlimited tries**. This saves us the trouble of having to reconnect multiple times and going through the 10s initial wait.

We modified the code (initially tried to exploit SecureRandom's weakness) to brute force all the combinations:

```
import java.io.*;
import java.net.*;

public class SecureBrute {
	public static void main(String[] args) throws Exception {
		Socket sk = new Socket("challenge.rgbsec.xyz", 7425);
		DataInputStream din = new DataInputStream(sk.getInputStream());
		DataOutputStream dout = new DataOutputStream(sk.getOutputStream());
		// Welcome
		String s = din.readLine();
		System.out.println(s);
		// Generating seed
		s = din.readLine();
		System.out.println(s);
		// Yesterday's numbers
		s = din.readLine();
		System.out.println(s);
		s = din.readLine();
		System.out.println(s);
		String[] tokens = s.split(" ");
		int[] nums = new int[5];
		for (int i = 0; i < 5; i++) {
			nums[i] = Integer.parseInt(tokens[i]);
		}
		// You have $20
		s = din.readLine();
		System.out.println(s);
		// Pwnage starts here
		dout.writeBytes("-1\n");
		dout.flush();
		
		int[] c = new int[5];
		loop:
		for (c[0] = 0; c[0] < 5; c[0]++)
		for (c[1] = 0; c[1] < 5; c[1]++)
		for (c[2] = 0; c[2] < 5; c[2]++)
		for (c[3] = 0; c[3] < 5; c[3]++)
		for (c[4] = 0; c[4] < 5; c[4]++) {
			boolean done = tryCombo(c, din, dout);
			if (done) break loop;
		}
		
		din.close();
		dout.close();
		sk.close();
	}
	
	private static boolean tryCombo(int[] combo,
		DataInputStream din,
		DataOutputStream dout) throws Exception {
		// Ticket number
		String s = din.readLine();
		System.out.println(s);
		String next5 = getNextFive(combo);
		System.out.println(next5);
		dout.writeBytes(next5 + "\n");
		dout.flush();
		s = din.readLine();
		System.out.println(s);
		if (s.startsWith("Congratulations")) {
			for (int i = 0; i < 100; i++) {
				s = din.readLine();
				System.out.println(s);
			}
			return true;
		}
		return false;
	}
	
	private static String getNextFive(int[] combo) {
		String result = "";
		for (int i = 0; i < 4; i++) {
			result += (combo[i] + 1) + " ";
		}
		result += combo[4] + 1;
		return result;
	}
}
```

And got the flag after 1220 tries:

```
Ticket number 1218! Enter five numbers, separated by spaces:
2 5 4 4 3
Your ticket did not win. Try again.
Ticket number 1219! Enter five numbers, separated by spaces:
2 5 4 4 4
Your ticket did not win. Try again.
Ticket number 1220! Enter five numbers, separated by spaces:
2 5 4 4 5
Congratulations, you win the flag lottery!
rgbCTF{s0m3t1m3s_4ll_y0u_n33d_1s_f0rc3}
```

Flag: `rgbCTF{s0m3t1m3s_4ll_y0u_n33d_1s_f0rc3}`
