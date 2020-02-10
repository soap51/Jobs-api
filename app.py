# app.py
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import re
import spacy
import pandas as pd
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from flask_cors import CORS, cross_origin
from spacy.tokens import Doc
from spacy.vocab import Vocab
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class CustomTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        new_vocabs = [
            " R ",
            "R, ",
            ", R",
            "Hadoop",
            "Big Data",
            "Big data",
            "big data",
            "Data",
            "data",
            "Business",
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
            "ERP",
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
            "Sql",
            "sql",
            "Data Studio", 
            "Google Analytics", 
            "Amazon Web Services", 
            "AWS", 
            "Amazon Web Service",
            "MongoDB", 
            "NoSQL",
            "Nosql",
            "nosql",
            "NOSQL",  
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
            "docker",
            "kubernetes",
            "Google Cloud",
            "SAS",
            "Logistic Regression",
            "KNN",
            "k-Nearest Neighbor",
            "MXNet",
            "pandas",
            "information retrieval",
            "Information Retrieval",
            "data visualization",
            "nodejs",
            "Nodejs",
            "Node.js",
            "node.js",
            "python",
            "Python",
            "Redis",
            "Golang",
            "Java",
            "C++",
            "C#",
            "J2EE",
            "JSP",
            "Servlet",
            "JQuery",
            "JSF",
            "Hibernate",
            "JDBC",
            "Apache tomcat",
            "Maven",
            "Oracle database",
            "Agile",
            "SCRUM",
            "REST API",
            "Rest Api",
            "react",
            "HTML",
            "html",
            "Css",
            "CSS",
            "Angular",
            "Vue"
        ]
        words = text.split(' ')
        empty_doc = Doc(self.vocab ,words=words)       
        for word in new_vocabs:    
            empty_doc.vocab.strings.add(word)
   
        return empty_doc


@app.route('/<string:occupation>' , methods=["GET"])
@cross_origin()
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
    nlp.tokenizer = CustomTokenizer(nlp.vocab)
    for a in posLinks:
        html_jobs = requests.get(a["href"]).text
        soup_jobs = BeautifulSoup(html_jobs ,features="html.parser")  
        div_jobs_detail = soup_jobs.find("div", class_="jobad-primary-details")
        clean_re = re.compile(' {2, }|<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  
        plain_text_jobs_detail = re.sub(clean_re, '',  str(div_jobs_detail))       
        plain_text_jobs_detail = " ".join(plain_text_jobs_detail.split())
        
       
 
        text_token = nlp(plain_text_jobs_detail) 
        for w in text_token:
            print(w)
            lexme = nlp.vocab[w.text]
            if lexme.is_stop == False and w.lemma_.isalpha() :                                           
                word = w.lemma_.lower()                                  
                if (word in count_dict):                               
                    count_dict[word] += 1       
        
                else:                                   
                    count_dict[word] = 1 
    
    df = pd.DataFrame.from_dict(count_dict, columns=["count"], orient="index")
    
    return jsonify((df.sort_values(["count"], ascending=False).to_json() ))

# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)