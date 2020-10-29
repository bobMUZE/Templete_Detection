import requests
from bs4 import BeautifulSoup

## HTTP GET Request
req = requests.get('https://owasp.org/www-community/xss-filter-evasion-cheatsheet')


## HTML 소스 가져오기
html = req.text
soup = BeautifulSoup(html, 'html.parser')

codes = soup.select(
    'code'
    )
with open("xss_attack.txt","a",encoding='utf-8') as f:

    for code in codes:
        f.write(code.text+"\n")
        #print(code.text,"\n")
