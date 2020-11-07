#이벤트 핸들러랑, 태그를 CSV파일로 저장

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

PortSwigger_URL="https://portswigger.net/web-security/cross-site-scripting/cheat-sheet"

driver = webdriver.Chrome('C:\\webdriver\\chromedriver')
driver.get(PortSwigger_URL)
not_requires = driver.find_elements_by_css_selector('body > section.maincontainer > div > details.xss-cheat-sheet-container-eventhandlers > div > \
                                            details:nth-child(2) > div > details')

#requires = driver.find_elements_by_css_selector('body > section.maincontainer > div > details.xss-cheat-sheet-container-eventhandlers > div > \
#                                            details:nth-child(3) > div > details')
file_name="not_require.csv"
#file_name="require.csv"
f = open(file_name, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

for i in not_requires:
    event_text=i.find_element_by_tag_name("summary").text
    #print(event_text)
    options = i.find_elements_by_tag_name("option")
    # f.writelines()
    for option in options:
        #option.click()
        #time.sleep(0.5)
        # driver.implicitly_wait(2)
        # print (option.text)
        option_text=option.text
        if option_text!='custom tags':
            wr.writerow([event_text,option_text])
            #print([event_text,option_text])
driver.close()
f.close()