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
