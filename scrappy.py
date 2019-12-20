import time
from selenium import webdriver
import requests
import bs4
from bs4 import BeautifulSoup
driver = webdriver.Chrome('./chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://th.jobsdb.com/th')
time.sleep(4) # Let the user actually see something!
driver.find_element_by_id('SecondaryLanguageButton').click()
search_text = driver.find_element_by_name('keywordInput')
search_text.send_keys('data scientist')
driver.find_element_by_id('searchbox-submit').click()
position_links = driver.find_elements_by_class_name("posLink")
for link in position_links:
    url = link.get_attribute("href")
    data = requests.get(url).text
    soup = BeautifulSoup(data ,features="html.parser")
    div = soup.find_all("div", class_="jobad-primary-details")[0]
    span = div.find("span")     
    for ul in span.find_all("ul"):
        for li in ul.find("li"):               
            try:                      
                if isinstance(li, type(None)) and type(li) == bs4.element.NavigableString or type(li) == bs4.element.Tag:
                    print(li)
                    if len(li.string) != 1:
                        
                        print(li.content)
                pass
            except (AttributeError, TypeError) as e:
                print("Ignores ",e)
                pass
       
  
time.sleep(5) # Let the user actually see something!
driver.quit()