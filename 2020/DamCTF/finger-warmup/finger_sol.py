import requests
from bs4 import BeautifulSoup

URL = "https://finger-warmup.chals.damctf.xyz/"

def get_data(path):
    r = requests.get(url = URL + path)
    if not 'click here' in r.text:
        print(r.text)
        return True, r.text
    soup = BeautifulSoup(r.text, features="html.parser")
    path = soup.a.get('href')
    print(path)
    return False, path

found = False
path = 'un5vmavt8u5t5op1u94h'
path = 'plcs3v3yfyovawuov9bh4e'
while not found:
    found, path = get_data(path)

#Nice clicking, I'm very impressed! Now to go onwards and upwards! <br/><pre>dam{I_hope_you_did_this_manually}</pre>
