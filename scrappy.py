import time
from selenium import webdriver
import requests
import bs4
from bs4 import BeautifulSoup
import deepcut
from nltk.corpus import stopwords 
from selenium.common.exceptions import NoSuchElementException
import json
import os
import re
import pandas as pd
import csv
import collections
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

driver = webdriver.Chrome('./chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://th.jobsdb.com/th/th')
stop_words = set(stopwords.words('english')) 
time.sleep(0) # Let the user actually see something!
driver.find_element_by_id('SecondaryLanguageButton').click()
print(driver.find_element_by_id('SecondaryLanguageButton'))
search_text = driver.find_element_by_name('keywordInput')
keyword = "data scientist"
#keyword = "data engineer"
search_text.send_keys(keyword)
driver.find_element_by_id('searchbox-submit').click()
result = []
custom_dict = [
    " R ",
    "R, ",
    ", R",
    "Hadoop",
    "Big Data",
    "Machine Learning",
    "machine learning",
    "Deep Learning",
    "deep learning",
    "Neural Network",
    "neural network",
    "Neural Networks",
    "neural networks",       
    "Computer Vision",
    "Data Mining", 
    "data mining",
    "Text Mining", 
    "text mining", 
    "Tableau", 
    "tableau",     
    "Data Scientist",
    "Python",
    "Javascript",
    "PowerBI", 
    "Power BI", 
    "power bi", 
    "SQL",         
    "Data Studio", 
    "Google Analytics", 
    "Amazon Web Services", 
    "AWS", 
    "Amazon Web Service",
    "MongoDB", 
    "NoSQL",  
    "hive",
    "Hive",
    "HIVE",
    "apache hive",
    "Apache Hive",
    "Apache Pig",
    "Pig",
    "PIG",
    "Spark",
    "Apache Spark",
    "Apache spark",
    "apache spark",
    "HDFS",
    "Hadoop Distributed File System",
    "Hbase",
    "Sqoop",
    "ZooKeeper",
    "Apache ZooKeeper",
    "Apache Airflow",
    "NOSQL",
    "MapReduce",
    "Solr",
    "Lucene",
    "C++",
    "Artificial Intelligence",
    "AI",
    "Expert Systems",
    "Scala",
    "Java",
    "Natural Language Processing",
    "natural language processing",
    "Pattern Recognition",
    "pattern recognition",
    "Recommendation Systems",
    "recommendation systems",
    "BigQuery",
    "Cassandra",
    "ElasticSearch",
    "Kafka",
    "Flask",
    "Caffe",
    "Torch",
    "Scikit-Learn",
    "Theano",
    "MLlib",
    "Classification",
    "Regression",
    "Clustering",
    "Association Rules",
    "Support Vector Machines",
    "support vector machines",
    "Storm",
    "Azkaban",
    "Luigi",
    "Tensorflow",
    "Keras",
    "Pytorch",
    "BigQuery",
    "Dataproc",
    "ML Engine",
    "Google Cloud",
    "SAS",
    "Logistic Regression",
    "KNN",
    "k-Nearest Neighbor",
    "MXNet",
    "pandas",
    "information retrieval",
    "Information Retrieval",
    "data visualization"
]
has_data = True
count_dict = {}
df = pd.DataFrame(columns=["Name","Count"])

try :
    while has_data :
        position_links = driver.find_elements_by_class_name("posLink")     
        for link in position_links:        
            url = link.get_attribute("href")
            data = requests.get(url).text
            soup = BeautifulSoup(data ,features="html.parser")            
            time.sleep(4) 
            div = soup.find_all("div", class_="jobad-primary-details")[0]
            span = div.find("span")     
            cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            detail = re.sub(cleanr, '', str(div))                 
            detail = detail.replace("\r\n", "")
            detail = detail.replace("\n", "")
            detail = detail.replace(u'\xa0', u' ')
            #print("----")
            filtered_word = []    

            text_token = deepcut.tokenize(detail , custom_dict=custom_dict)
            text_token = [text for text in text_token if text.isalnum()]
            #print(text_token)
            #print("----")      
            for w in text_token: 
                if w not in stop_words: 
                    if w not in count_dict:
                        count_dict[w] = 1
                    else:
                        count_dict[w] += 1

            # counter=collections.Counter(filtered_word)
            # print(counter)
           
            # print(counter.values())
     
            # print(counter.keys())
            
            # print(counter.most_common(3))

            #join_word = " ".join(filtered_word)           
            #result.append({"keyword": keyword , "detail" : join_word})
        if driver.get(driver.find_element_by_class_name("pagebox-next").get_attribute("href")) != "":
            has_data = True
        else :
            has_data = False
except (NoSuchElementException) as e:
    print(e)

# print(result)
# print(len(result))

print(count_dict)

for key, value in count_dict.items():
    


time.sleep(10) # Let the user actually see something!
driver.quit()
