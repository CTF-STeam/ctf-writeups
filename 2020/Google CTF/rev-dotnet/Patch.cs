// OSTRON.KVOT
// Token: 0x06000153 RID: 339
private void submit_button_Click(object sender, EventArgs e)
{
	int[] list = { 48,25,23,19,15,26,13,57,36,9,52,27,4,18,49,6,41,8,43,62,45,55,37,32,1,0,7,28,47,2 };
	string alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}";
	string result = "";
	for (int i = 0; i < 30; i++)
	{
		int pos = this.FindShuffledPosition(i);
		foreach (char c in alpha)
		{
			string input = CreateInput(i, c);
			string[] output = KVOT.FYRKANTIG(input).Split('-');
			if (Convert.ToInt32(output[pos]) == list[pos])
			{
				result += c;
			}
		}
	}
	this.information_label.Text = result;
}
private string CreateInput(int pos, char c)
{
	string res = "";
	for (int i = 0; i < 30; i++)
	{
		if (i != pos)
		{
			res += "1";
		}
		else
		{
			res += c;
		}
	}
	return res;
}
private int FindShuffledPosition(int pos)
{
	string[] output = KVOT.FYRKANTIG(this.CreateInput(pos, '1')).Split('-');
	string[] output2 = KVOT.FYRKANTIG(this.CreateInput(pos, '2')).Split('-');
	for (int i = 0; i < 30; i++)
	{
		if (output[i] != output2[i])
		{
			return i;
		}
	}
	return -1;
}
