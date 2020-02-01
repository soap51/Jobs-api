from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import re
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

import time
app = Flask(__name__)

@app.route('/<string:occupation>')
def getData(occupation):
    nlp =  English()
    source = requests.get("https://th.jobsdb.com/TH/TH/Search/FindJobs?KeyOpt=COMPLEX&JSRV=1&RLRSF=1&JobCat=1&SearchFields=Positions,Companies&Key="+occupation+"&JSSRC=HPSS").text
    soup = BeautifulSoup(source ,features="html.parser")  
    links = []
    poslink = soup.find_all("a",class_="posLink" )
    link_next_page = soup.find("a",class_="pagebox-next" )
    posLinks = []
    posLinks.extend(poslink)    
    while( not((link_next_page) is None) and link_next_page.get("href") != ""):      
        links.append(link_next_page.get("href"))
        temp_source = requests.get(link_next_page.get("href")).text
        temp_soup = BeautifulSoup(temp_source ,features="html.parser")
        link_next_page = temp_soup.find("a",class_="pagebox-next" ) 
        poslink = temp_soup.find_all("a",class_="posLink" ) 
        posLinks.extend(poslink)          
    count_dict= {}
    word = ""
    for a in posLinks:
        html_jobs = requests.get(a["href"]).text
        soup_jobs = BeautifulSoup(html_jobs ,features="html.parser")  
        div_jobs_detail = soup_jobs.find("div", class_="jobad-primary-details")
        clean_re = re.compile(' {2, }|<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  
        plain_text_jobs_detail = re.sub(clean_re, '',  str(div_jobs_detail))       
        plain_text_jobs_detail = " ".join(plain_text_jobs_detail.split())
        text_token = nlp(plain_text_jobs_detail)        
        for w in text_token:
            lexme = nlp.vocab[w.text]
            if lexme.is_stop == False and w.lemma_.isalpha() :                                           
                word = w.lemma_.lower()                                  
                if (word in count_dict):                               
                    count_dict[word] += 1             
                else:                                   
                    count_dict[word] = 1                                         
    return jsonify(count_dict)


if __name__ == "__main__":
    app.run()