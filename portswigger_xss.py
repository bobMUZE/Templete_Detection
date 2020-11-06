from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

PortSwigger_URL="https://portswigger.net/web-security/cross-site-scripting/cheat-sheet"
file_name="XSS_Event_handle"
driver = webdriver.Chrome('C:\\webdriver\\chromedriver')
kernel32_file=open(file_name,"a")
driver.get(PortSwigger_URL)
not_requires = driver.find_elements_by_css_selector('body > section.maincontainer > div > details.xss-cheat-sheet-container-eventhandlers > div > \
                                            details:nth-child(3) > div > details')

with open("tag_event.txt","a",encoding="utf-8") as f:
    f.write("1")
    for i in not_requires:
        options=i.find_elements_by_tag_name("option")
        #f.writelines()
        for option in options:
            option.click()
            time.sleep(0.5)
            #driver.implicitly_wait(2)
            #print (option.text)
            print(i.find_element_by_tag_name("a").text)
            f.write(i.find_element_by_tag_name("a").text)


        #print(i.find_element_by_tag_name("a").text)


driver.close()
