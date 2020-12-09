import modsec_parser
import requests
from bs4 import BeautifulSoup

URL="http://218.146.55.65/wordpress/index.php/about/?uid=4&mod=document&pageid=1"
SELECTOR = "#kboard-default-document > div.kboard-document-wrap > div.kboard-content"
TEMPLETE_JSON = {'time': '1605365247.624045',
                 'url': 'http://3.131.17.188/g5', 'module': 1,
                 'filepath': '/home/ubuntu/semicrawling/3.131.17.188/g5/0',
                 'xpath': '//*[@id="hd"]',
                 'response':"200"
                 }

req = requests.get(URL)
html = req.text
soup = BeautifulSoup(html, 'html.parser')
content = soup.select(SELECTOR)
modsec_parser.main(content,TEMPLETE_JSON)

