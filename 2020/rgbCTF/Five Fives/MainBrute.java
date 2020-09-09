import java.util.*;
import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.util.concurrent.ThreadLocalRandom;
import java.security.*;

public class MainBrute {
	static int[] nums = null;
	public static void main(String[] args) throws Exception {
		nums = new int[5];
		trySolve(1000);
		//server();
	}
	
	private static boolean trySolve(int delta) throws Exception {
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
		for (int i = 0; i < 5; i++) {
			nums[i] = Integer.parseInt(tokens[i]);
		}
		// You have $20
		s = din.readLine();
		System.out.println(s);
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
		return false;
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
	
	private static boolean match(long seed) {
		ByteBuffer bb = ByteBuffer.allocate(Long.BYTES);
		bb.putLong(seed);
		SecureRandom r = new SecureRandom(bb.array());
		for (int i = 0; i < 5; i++) {
			int n = r.nextInt(5) + 1;
			if (n != nums[i]) {
				return false;
			}
		}
		return true;
	}
	
	private static long findSeed(long initSeed) {
		long seed = initSeed - 1;
		while (!match(seed)) {
			seed--;
		}
		return seed;
	}
	
	private static String getNextFive(long seed) {
		ByteBuffer bb = ByteBuffer.allocate(Long.BYTES);
		bb.putLong(seed);
		SecureRandom r = new SecureRandom(bb.array());
		for (int a = 0; a < 5; a++) {
			r.nextInt(5);
		}
		String result = "";
		for (int i = 0; i < 5; i++) {
			result += r.nextInt(5) + 1;
			if (i < 4) result += " ";
		}
		return result;
	}
	
	private static String getNextFive(int[] combo) {
		String result = "";
		for (int i = 0; i < 4; i++) {
			result += (combo[i] + 1) + " ";
		}
		result += combo[4] + 1;
		return result;
	}
	
	public static void server() throws Exception {
		Scanner in = new Scanner(System.in);
		
		System.out.println("Welcome to the Five Fives Lotto!");
		System.out.println("Generating seed...");
		
		//You'll never find my seed now!
		int sleep = ThreadLocalRandom.current().nextInt(1000);
		//Thread.sleep(sleep);
		long seed = System.currentTimeMillis();
		seed = 1594561504667L;
		System.out.println(seed);
		ByteBuffer bb = ByteBuffer.allocate(Long.BYTES);
		bb.putLong(seed);
		SecureRandom r = new SecureRandom(bb.array());
		Thread.sleep(1000 - sleep);
		
		System.out.println("Yesterday's numbers were: ");
		for (int i = 0; i != 5; i++) {
			System.out.print((r.nextInt(5000) + 1) + " ");
		}
		System.out.println();
		
		System.out.println("You have $20, and each ticket is $1. How many tickets would you like to buy? ");
		int numTries = Integer.parseInt(in.nextLine());
		if (numTries > 20) {
			System.out.println("Sorry, you don't have enough money to buy all of those. :(");
			System.exit(0);
		}
		
		int[] nums = new int[5];
		for (int a = 0; a != 5; a++) {
			nums[a] = r.nextInt(5000) + 1;
			System.out.print(nums[a] + " ");
		}
		System.out.println();
		
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
	}

	public static void outputFlag() {
		try {
			BufferedReader in = new BufferedReader(new FileReader("flag.txt"));
			System.out.println(in.readLine());
		} catch (IOException e) {
			System.out.println("Error reading flag. Please contact admins.");
		}
	}
}
