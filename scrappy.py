import time
from selenium import webdriver
import requests
import bs4
from bs4 import BeautifulSoup
import deepcut
import os
import re
import pandas as pd
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

driver = webdriver.Chrome('./chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://th.jobsdb.com/th/th')
time.sleep(0) # Let the user actually see something!
driver.find_element_by_id('SecondaryLanguageButton').click()
search_text = driver.find_element_by_name('keywordInput')
keyword = "data scientist"
search_text.send_keys(keyword)
driver.find_element_by_id('searchbox-submit').click()
position_links = driver.find_elements_by_class_name("posLink")
result = []
for link in position_links:
   
    url = link.get_attribute("href")
    data = requests.get(url).text
    soup = BeautifulSoup(data ,features="html.parser")    
    time.sleep(5) 
    div = soup.find_all("div", class_="jobad-primary-details")[0]
    span = div.find("span")     
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    detail = re.sub(cleanr, '', str(div))                 
    detail = detail.replace("\r\n", "")
    detail = detail.replace("\n", "")
    detail = detail.replace(u'\xa0', u' ')
    #print(detail)
    result.append({"keyword": keyword , "detail" : detail})
    print("----")    
    text_token = deepcut.tokenize(detail)
    print(text_token)
    print("----")
   
  
time.sleep(5) # Let the user actually see something!
driver.quit()