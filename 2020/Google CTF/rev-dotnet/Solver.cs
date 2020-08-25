using System;
using System.Collections.Generic;

public class Solver
{
	private static string FYRKANTIG(string BISSING)
	{
		List<uint> list = null;
		if (BISSING.Length != 30)
		{
			return "Flag must be exactly 30 characters long. Please check the number and try again.";
		}
		list = GRUNDTAL_NORRVIKEN(BISSING);
		int num = 0;
		if (0 < list.Count)
		{
			do
			{
				if (list[num] <= 63)
				{
					num++;
					continue;
				}
				return string.Concat("Unexpected character " + BISSING[num], "; Characters must be in the set {A-Za-z0-9}. Please check the number and try again.");
			}
			while (num < list.Count);
		}
		List<uint> list2 = new List<uint>(30);
		list2.Add(18u);
		list2.Add(43u);
		list2.Add(47u);
		list2.Add(5u);
		list2.Add(35u);
		list2.Add(44u);
		list2.Add(59u);
		list2.Add(17u);
		list2.Add(3u);
		list2.Add(21u);
		list2.Add(6u);
		list2.Add(43u);
		list2.Add(44u);
		list2.Add(37u);
		list2.Add(26u);
		list2.Add(42u);
		list2.Add(24u);
		list2.Add(34u);
		list2.Add(57u);
		list2.Add(14u);
		list2.Add(30u);
		list2.Add(5u);
		list2.Add(16u);
		list2.Add(23u);
		list2.Add(37u);
		list2.Add(49u);
		list2.Add(48u);
		list2.Add(16u);
		list2.Add(28u);
		list2.Add(49u);
		DAGSTORP(ref list, list2);
		for (int i = 0; i < list.Count; i++)
		{
			Console.WriteLine(i + " " + list[i]);
		}
		if (!SMORBOLL(list))
		{
			return "Flag checksum invalid. Please check the number and try again.";
		}
		return HEROISK(list);
	}
	public static List<uint> GRUNDTAL_NORRVIKEN(string LINNMON)
	{
		List<uint> list = new List<uint>(LINNMON.Length);
		int num = 0;
		if (0 < LINNMON.Length)
		{
			do
			{
				list.Add((uint)DecodeBase64Bytewise((sbyte)LINNMON[num]));
				num++;
			}
			while (num < LINNMON.Length);
		}
		return list;
	}
	public static string Base64Decode(List<uint> list)
	{
		string s = "";
		for (int i = 0; i < list.Count; i++)
		{
			s += (char)EncodeBase64Bytewise((sbyte)list[i]);
		}
		return s;
	}
	internal static sbyte DecodeBase64Bytewise(sbyte arg)
	{
		if ((uint)(byte)(arg + 208) <= 9u)
		{
			return (sbyte)(arg - 48);
		}
		if ((uint)(byte)(arg + 191) <= 25u)
		{
			return (sbyte)(arg - 55);
		}
		if ((uint)(byte)(arg + 159) <= 25u)
		{
			return (sbyte)(arg - 61);
		}
		int result;
		switch (arg)
		{
		case 123:
			return 62;
		default:
			result = -1;
			break;
		case 125:
			result = 63;
			break;
		}
		return (sbyte)result;
	}
	internal static sbyte EncodeBase64Bytewise(sbyte arg)
	{
		if (arg <= 9)
		{
			return (sbyte)(arg + 48);
		}
		if (arg <= 35)
		{
			return (sbyte)(arg + 55);
		}
		if (arg <= 61)
		{
			return (sbyte)(arg + 61);
		}
		int result;
		switch (arg)
		{
		case 62:
			return 123;
		default:
			result = -1;
			break;
		case 63:
			result = 125;
			break;
		}
		return (sbyte)result;
	}
	public static void DAGSTORP(ref List<uint> primary, List<uint> filter)
	{
		int num = 0;
		if (0 < primary.Count)
		{
			do
			{
				primary[num] = (filter[num % filter.Count] ^ primary[num]);
				num++;
			}
			while (num < primary.Count);
		}
	}
	internal static bool SMORBOLL(List<uint> IRMELIN)
	{
		if (IRMELIN.Count == 0)
		{
			return true;
		}
		uint num = 16u;
		int num2 = 0;
		if (0 < IRMELIN.Count)
		{
			do
			{
				if (num2 != IRMELIN.Count - 2)
				{
					int count = 0;
					num = IRMELIN[num2] + num;
					count++;
					if (num2 % 2 == 0)
					{
						num = IRMELIN[num2] + num;
						count++;
					}
					int num3 = num2;
					if (num3 - num3 / 3 * 3 == 0)
					{
						num = (uint)((int)IRMELIN[num2] * -2 + (int)num);
						count -= 2;
					}
					int num4 = num2;
					if (num4 - num4 / 5 * 5 == 0)
					{
						num = (uint)((int)IRMELIN[num2] * -3 + (int)num);
						count -= 3;
					}
					int num5 = num2;
					if (num5 - num5 / 7 * 7 == 0)
					{
						num = IRMELIN[num2] * 4 + num;
						count += 4;
					}
					//Console.WriteLine(num2 + " " + count);
				}
				num2++;
			}
			while (num2 < IRMELIN.Count);
		}
		return (uint)(sbyte)IRMELIN[IRMELIN.Count - 2] == (num & 0x3F);
	}
	internal static string HEROISK(List<uint> MATHOPEN)
	{
		string result = "Invalid flag. Please check the number and try again.";
		if (!VAXMYRA(MATHOPEN))
		{
			return result;
		}
		if (MATHOPEN[1] != 25)
		{
			return result;
		}
		if (MATHOPEN[2] != 23)
		{
			return result;
		}
		if (MATHOPEN[9] != 9)
		{
			return result;
		}
		if (MATHOPEN[20] != 45)
		{
			return result;
		}
		if (MATHOPEN[26] != 7)
		{
			return result;
		}
		if (MATHOPEN[8] < 15)
		{
			return result;
		}
		if (MATHOPEN[12] > 4)
		{
			return result;
		}
		if (MATHOPEN[14] < 48)
		{
			return result;
		}
		if (MATHOPEN[29] < 1)
		{
			return result;
		}
		int num = (int)MATHOPEN[4];
		int num2 = (int)MATHOPEN[3];
		int num3 = (int)MATHOPEN[2];
		int num4 = (int)MATHOPEN[1];
		if ((byte)(((uint)((int)MATHOPEN[0] + num4 + num + num3 + num2 - 130) <= 10u) ? 1 : 0) == 0)
		{
			return result;
		}
		num4 = (int)MATHOPEN[9];
		int num5 = (int)MATHOPEN[8];
		int num6 = (int)MATHOPEN[7];
		int num7 = (int)MATHOPEN[6];
		if ((byte)(((uint)((int)MATHOPEN[5] + num7 + num6 + num5 + num4 - 140) <= 10u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num8 = (int)MATHOPEN[14];
		int num9 = (int)MATHOPEN[13];
		int num10 = (int)MATHOPEN[12];
		int num11 = (int)MATHOPEN[11];
		if ((byte)(((uint)((int)MATHOPEN[10] + num11 + num10 + num9 + num8 - 150) <= 10u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num12 = (int)MATHOPEN[19];
		int num13 = (int)MATHOPEN[18];
		int num14 = (int)MATHOPEN[17];
		int num15 = (int)MATHOPEN[16];
		if ((byte)(((uint)((int)MATHOPEN[15] + num15 + num14 + num13 + num12 - 160) <= 10u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num16 = (int)MATHOPEN[24];
		int num17 = (int)MATHOPEN[23];
		int num18 = (int)MATHOPEN[22];
		int num19 = (int)MATHOPEN[21];
		if ((byte)(((uint)((int)MATHOPEN[20] + num19 + num18 + num17 + num16 - 170) <= 10u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num20 = (int)MATHOPEN[25];
		int num21 = (int)MATHOPEN[20];
		int num22 = (int)MATHOPEN[15];
		int num23 = (int)MATHOPEN[10];
		int num24 = (int)MATHOPEN[5];
		if ((byte)(((uint)((int)MATHOPEN[0] + num24 + num23 + num22 + num21 + num20 - 172) <= 6u) ? 1 : 0) == 0)
		{
			return result + "123";
		}
		int num25 = (int)MATHOPEN[26];
		int num26 = (int)MATHOPEN[21];
		int num27 = (int)MATHOPEN[16];
		int num28 = (int)MATHOPEN[11];
		int num29 = (int)MATHOPEN[6];
		if ((byte)(((uint)((int)MATHOPEN[1] + num29 + num28 + num27 + num26 + num25 - 162) <= 6u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num30 = (int)MATHOPEN[27];
		int num31 = (int)MATHOPEN[22];
		int num32 = (int)MATHOPEN[17];
		int num33 = (int)MATHOPEN[12];
		int num34 = (int)MATHOPEN[7];
		if ((byte)(((uint)((int)MATHOPEN[2] + num34 + num33 + num32 + num31 + num30 - 152) <= 6u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num35 = (int)MATHOPEN[23];
		int num36 = (int)MATHOPEN[18];
		int num37 = (int)MATHOPEN[13];
		int num38 = (int)MATHOPEN[8];
		if ((byte)(((uint)((int)MATHOPEN[3] + num38 + num37 + num36 + num35 - 142) <= 6u) ? 1 : 0) == 0)
		{
			return result;
		}
		int num39 = (int)MATHOPEN[29];
		int num40 = (int)MATHOPEN[24];
		int num41 = (int)MATHOPEN[19];
		int num42 = (int)MATHOPEN[14];
		int num43 = (int)MATHOPEN[9];
		if ((byte)(((uint)((int)MATHOPEN[4] + num43 + num42 + num41 + num40 + num39 - 132) <= 6u) ? 1 : 0) == 0)
		{
			return result;
		}
		uint num44 = MATHOPEN[27] * 3;
		uint num45 = (MATHOPEN[7] + num44) * 3 - MATHOPEN[5] * 13;
		if (num45 - 57 <= 28)
		{
			num44 = MATHOPEN[20] * 5;
			num44 = (MATHOPEN[14] << 2) - num44;
			num45 = MATHOPEN[22] * 3 + num44;
			if (num45 - 12 <= 70)
			{
				num44 = MATHOPEN[18] * 2;
				num44 = (MATHOPEN[15] - num44) * 3;
				uint num46 = MATHOPEN[16] * 2;
				num46 = (MATHOPEN[14] + num46) * 2 + num44 - MATHOPEN[17] * 5;
				if (MATHOPEN[13] + num46 != 0)
				{
					return result;
				}
				num46 = MATHOPEN[6] * 2;
				if (MATHOPEN[5] != num46)
				{
					return result;
				}
				if (MATHOPEN[29] + MATHOPEN[7] != 59)
				{
					return result;
				}
				uint num47 = MATHOPEN[17] * 6;
				if (MATHOPEN[0] != num47)
				{
					return result;
				}
				num47 = MATHOPEN[9] * 4;
				if (MATHOPEN[8] != num47)
				{
					return result;
				}
				num47 = MATHOPEN[13] * 3;
				if (MATHOPEN[11] << 1 != num47)
				{
					return result;
				}
				if (MATHOPEN[13] + MATHOPEN[29] + MATHOPEN[11] + MATHOPEN[4] != MATHOPEN[19])
				{
					return result;
				}
				uint num48 = MATHOPEN[12] * 13;
				if (MATHOPEN[10] != num48)
				{
					return result;
				}
				return null;
			}
			return result;
		}
		return result;
	}
	internal static bool VAXMYRA(List<uint> LYCKSELE)
	{
		int num = 0;
		if (0 < LYCKSELE.Count)
		{
			do
			{
				int num2 = 0;
				if (0 < num)
				{
					do
					{
						if (LYCKSELE[num] != LYCKSELE[num2])
						{
							num2++;
							continue;
						}
						return false;
					}
					while (num2 < num);
				}
				num++;
			}
			while (num < LYCKSELE.Count);
		}
		return true;
	}
	public static void Main()
	{
		List<uint> list = new List<uint>(30);
		uint[] listA = { 48,25,23,19,15,26,13,57,36,9,52,27,4,18,49,6,41,8,43,62,45,55,37,32,1,0,7,28,47,2 };
		foreach (uint n in listA)
			list.Add(n);
		if (!SMORBOLL(list))
		{
			Console.WriteLine("Flag checksum invalid. Please check the number and try again.");
		}
		Console.WriteLine("Hero: " + HEROISK(list));
		List<uint> list2 = new List<uint>(30);
		uint[] list2A = { 18,43,47,5,35,44,59,17,3,21,6,43,44,37,26,42,24,34,57,14,30,5,16,23,37,49,48,16,28,49 };
		foreach (uint n in list2A)
			list2.Add(n);
		DAGSTORP(ref list, list2);
		Console.WriteLine(Base64Decode(list));
		Console.WriteLine(FYRKANTIG("YouMissedSomethingImportantCpp"));
	}
}