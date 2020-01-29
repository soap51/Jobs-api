from flask import Flask
from bs4 import BeautifulSoup
import requests
import re
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lemmatizer import Lemmatizer
from spacy.lookups import Lookups
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    nlp =  English()
    lookups = Lookups()
    lookups.add_table("lemma_rules", {"noun": [["s", ""]]})
    lemmatizer = Lemmatizer(lookups)
    # Create a blank Tokenizer with just the English vocab
    #nlp.tokenizer = Tokenizer(nlp.vocab)
    source = requests.get("https://th.jobsdb.com/TH/TH/Search/FindJobs?KeyOpt=COMPLEX&JSRV=1&RLRSF=1&JobCat=1&SearchFields=Positions,Companies&Key=data%20engineer&JSSRC=HPSS").text
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
            if lexme.is_stop == False and w.text != "(" and w.text != ")" and w.text != ":" and w.text != "-"  :                                           
                word = w.lemma_.lower()                                  
                word = lemmatizer(word, "NOUN")[0]
                
                if (word in count_dict):                               
                    count_dict[word] += 1             
                else:                                   
                    count_dict[word] = 1    
             
                #print(word + " " +str(count_dict[word]))
                
        
    return count_dict