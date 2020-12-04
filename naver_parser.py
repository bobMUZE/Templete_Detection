import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver

NAVER_URL="https://blog.naver.com"
START_BRAVOTEC_URL="https://blog.naver.com/ljb1202/222161406981"
CONTENT_FILE="naver_blog_content.json"
NEXT_TAG_SELECTOR='#post-view222161406981 > div > div.se-main-container'

driver = webdriver.Chrome('C:\\webdriver\\chromedriver')
driver.implicitly_wait(5)
driver.get(START_BRAVOTEC_URL)
blog_content = driver.find_elements_by_class_name('se-main-container')
print(blog_content)

def content_parser(url):
    req = requests.get(url)
    html = req.text
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    content=soup.find(class_="se-main-container")
    print(content)
    content_str = str(content)
    #print(str(content))
    result={"url":url,"content":content_str}
    json_file = open(CONTENT_FILE, "a", encoding="utf-8")
    json.dump(result, json_file )
    json_file.write("\n")
    json_file.close()
    return soup,html

#content,html = content_parser(START_BRAVOTEC_URL)