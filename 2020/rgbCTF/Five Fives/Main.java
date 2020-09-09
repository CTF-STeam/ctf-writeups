import java.util.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.util.concurrent.ThreadLocalRandom;
import java.security.*;

public class Main {
	static int[] nums = null;
	public static void main(String[] args) throws Exception {
		System.out.println(args[0]);
		String[] tokens = args[0].split(",");
		nums = new int[5];
		for (int i = 0; i < 5; i++) {
			nums[i] = Integer.parseInt(tokens[i]);
		}
		long seed = System.currentTimeMillis() + 100000;
		for (int i = 0; i < 20; i++) {
			seed = findSeed(seed, 0);
		}
		//server();
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
	
	private static long findSeed(long initSeed, int count) {
		long seed = initSeed - 1;
		while (!match(seed)) {
			seed--;
		}
		System.out.print(seed + " " + count + "  ");
		ByteBuffer bb = ByteBuffer.allocate(Long.BYTES);
		bb.putLong(seed);
		SecureRandom r = new SecureRandom(bb.array());
		for (int i = 0; i <= count; i++) {
			for (int a = 0; a < 5; a++) {
				r.nextInt(5);
			}
		}
		for (int i = 0; i < 5; i++) {
			System.out.print((r.nextInt(5) + 1) + " ");
		}
		System.out.println();
		return seed;
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
