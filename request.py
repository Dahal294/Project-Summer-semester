import requests 
import json
import xml.etree.ElementTree as ET
import re
import pandas as pd
import string
import nltk

from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

string.punctuation
nltk.download('stopwords')
nltk.download('wordnet')

retmax = 10
base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
stopwords = nltk.corpus.stopwords.words('english')
porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()


def get_pmid(query, base_url = base_url, retmax = retmax):  
    esearch_url = f'{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax={retmax}'
    response = requests.get(esearch_url)
    if response.status_code == 200:
        pmids = response.json()['esearchresult']['idlist']
    for i, pmid in enumerate(pmids): 
        pmids[i] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"    
    df = pd.DataFrame(pmids, columns = ["PMID"])       
    return df


def get_abstract(df): 
    abstracts = []
    for row in df.iloc[:, 0]:
        response = requests.get(row)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            tags = soup.find_all("p")[3:8]
            pgh =''
            for p in tags: 
                pgh += " " + p.text 
            abstracts.append(pgh)
    df["abstracts"] = abstracts
    return df 


def get_topics(df):
    topics = []
    for row in df.iloc[:, 0]:
        response = requests.get(row)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            h1_tag = soup.find("h1")
            if h1_tag:
                topics.append(h1_tag.text)
            else:
                topics.append("No topic found")
        else:
            topics.append("Failed to retrieve")
    df["topics"] = topics
    return df













