import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
NAVER_BLOG_URL="https://blog.naver.com"
START_BLOG_URL="https://blog.naver.com/ljb1202/221226027421"
#START_BLOG_URL="https://blog.naver.com/ljb1202/222139365882"
CONTENT_FILE="naver_blog_content.json"
NEXT_PAGE_ID='postBottomTitleListBody'
DRIVER = webdriver.Chrome('C:\\webdriver\\chromedriver')
DRIVER.implicitly_wait(2)

def clawling_strat():
    DRIVER.get(START_BLOG_URL)
    #req = requests.get(START_BLOG_URL)
    #html = req.text
    #print(html)
    #soup = BeautifulSoup(html, 'html.parser')
    start_url =DRIVER.find_element_by_id("mainFrame").get_attribute("src")
    return start_url
    #content = soup.find("iframe",attrs={"id": "mainFrame"})
    #start_url = NAVER_BLOG_URL+content.attrs['src']
    #return start_url

    #blog_content = DRIVER.find_elements_by_tag_name('iframe')
    #start_blog_url = blog_content[0].get_attribute('src')
    #print(start_blog_url)
    #DRIVER.get(start_blog_url)
    #return start_blog_url

def content_parser(url):
    DRIVER.get(url)
    html = DRIVER.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content=soup.find(class_="se-main-container")
    #print(content)
    content_str = str(content)
    #print(str(content))
    result={"url":url,"content":content_str}
    #print(result)

    json_file = open(CONTENT_FILE, "a", encoding="utf-8")
    json.dump(result, json_file )
    json_file.write("\n")
    json_file.close()
    return html

def Next_Url(html):
    soup = BeautifulSoup(html, 'html.parser')
    #print(html)
    tags = soup.select("#postBottomTitleListBody > tr")
    #print(html)

    #print(tags)
    #count = 0
    check = False
    #total = len(tags)
    for tag in tags:
        #print(tag)
        #count+=1

        if check:

            next_url =NAVER_BLOG_URL+tag.find("a")["href"]
            print(next_url)
            return next_url

        if tag["class"]==["on"]:
            check=True

            #print(2)
    return False



    #return result

def main():
    start_url = clawling_strat()
    while start_url:
        html = content_parser(start_url)
        time.sleep(1.5)
        next_url = Next_Url(html)
        #break
        start_url = next_url

    print(start_url)
        #print(start_url)



if __name__ == '__main__':
    main()
