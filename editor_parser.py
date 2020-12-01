import requests
from bs4 import BeautifulSoup
import json

BRAVOTEC_URL="https://bravotec.co.kr/bbs"
START_BRAVOTEC_URL="https://bravotec.co.kr/bbs/board.php?bo_table=notice&wr_id=993"
CONTENT_FILE="bravotec_content.json"
NEXT_TAG_SELECTOR='#thema_wrapper > div.at-body > div > div > div > div.view-btn.text-right > div.btn-group > a'

def content_parser(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    content=soup.find("article")
    content_str = str(content)
    #print(str(content))
    result={"url":url,"content":content_str}
    json_file = open(CONTENT_FILE, "a", encoding="utf-8")
    json.dump(result, json_file )
    json_file.write("\n")
    json_file.close()
    return soup,html

def next_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select(NEXT_TAG_SELECTOR)
    for tag in tags:
        if tag.text.strip() == "다음":
            result= BRAVOTEC_URL + tag["href"][1:]
            break
        else:
            result = None

    return result


#req= requests.get(start_bravotec_url)
#html = req.text
content,html = content_parser(START_BRAVOTEC_URL)
next_link=next_url(html)

while(next_link):
    content,html = content_parser(next_link)
    next_link = next_url(html)
    print(next_link)


#게시판 리스트 URL



