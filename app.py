from flask import Flask
from bs4 import BeautifulSoup
import requests
import re
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    nlp =  English()
    # Create a blank Tokenizer with just the English vocab
    #nlp.tokenizer = Tokenizer(nlp.vocab)
    source = requests.get("https://th.jobsdb.com/TH/TH/Search/FindJobs?KeyOpt=COMPLEX&JSRV=1&RLRSF=1&JobCat=131&JSSRC=HPSS").text
    soup = BeautifulSoup(source ,features="html.parser")  
    all_a_tag = soup.find_all("a",class_="posLink" )   
    count_dict= {}
    word = ""
    for a in all_a_tag:
        html_jobs = requests.get(a["href"]).text
        soup_jobs = BeautifulSoup(html_jobs ,features="html.parser")  
        div_jobs_detail = soup_jobs.find("div", class_="jobad-primary-details")
        clean_re = re.compile(' {2, }|<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  
        plain_text_jobs_detail = re.sub(clean_re, '',  str(div_jobs_detail))       
        plain_text_jobs_detail = " ".join(plain_text_jobs_detail.split())
        text_token = nlp(plain_text_jobs_detail)
        for w in text_token:
            lexme = nlp.vocab[w.text]
            if lexme.is_stop == False:         
                if w.text in count_dict and not w.text.isalnum() :                               
                    if w.text == "Database" or w.text == "databases" or w.text == "database": 
                        print(w.text)                       
                        word = "database"         
                    else :
                        word = w.text.lower()      
                    count_dict[word] += 1
                    print(count_dict)
                    time.sleep(4)
                else:                 
                    if w.text == "Database" or w.text == "databases" or w.text == "database":
                        print(w.text)                       
                        word = "database"                              
                    else :
                        word = w.text.lower()
                            
                    count_dict[word] = 1                                             
                    print(count_dict)
                    time.sleep(4)
                
        
    return count_dict