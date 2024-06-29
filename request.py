import requests 
import json
import xml.etree.ElementTree as ET
<<<<<<< HEAD
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

retmax = 50
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


def remove_punctuation(text):
        punctuationfree="".join([i for i in text if i not in string.punctuation])
        return punctuationfree


def tokenization(text):
    tokens = re.split('\W+',text)
    return tokens


def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

def stemming(text):
    stem_text = [porter_stemmer.stem(word) for word in text]
    return stem_text


def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text

def remove_non_alpha(text):
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def preprocess(df):
#storing the puntuation free text
    df['clean_msg']= df['abstracts'].apply(lambda x:remove_punctuation(x))
    df['clean_msg']= df['clean_msg'].apply(lambda x: x.lower())
    df['clean_msg'] = df["clean_msg"].apply(lambda x:remove_non_alpha(x))
    df['clean_msg']= df['clean_msg'].apply(lambda x: tokenization(x))
    df['clean_msg']= df['clean_msg'].apply(lambda x:remove_stopwords(x))
    df['clean_msg']=df['clean_msg'].apply(lambda x: stemming(x))
    df['clean_msg']=df['clean_msg'].apply(lambda x:lemmatizer(x))
    df['clean_msg'] = df['clean_msg'].apply(lambda x: " ".join(x))
    return df




















# def get_result(query):
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
#     database = "pubmed"
#     retmax = 200
#     url = f"{base_url}esearch.fcgi?db={database}&term={query}&retmax={retmax}&usehistory=y"
#     response = requests.get(url)    
#     if response.status_code == 200:
#         root = ET.fromstring(response.text)
#         web_env = root.find('WebEnv').text
#         print(web_env)
#         query_key = root.find("QueryKey").text
#         print(query_key)
#         efetch_url = f"{base_url}efetch.fcgi?db={database}&query_key={query_key}&retmax={retmax}&WebEnv={web_env}&rettype=abstract&retmode=text&idtype=pmid"
#         Response = requests.get(efetch_url)
#         abstracts_data = Response.text
#         pmid_pattern = r'\bPMID:\s+\d+\b'
#         pmids = re.findall(pmid_pattern, abstracts_data)
#         for i, pmid in enumerate(pmids):
#          pmids[i] = pmid.replace("PMID: ", "")
#         for i, pmid in enumerate(pmids):
#             pmids[i] = f"<a>https://pubmed.ncbi.nlm.nih.gov/{pmid}/</a>"
#         fragments = re.split(pmid_pattern, abstracts_data) 
        
#         df = pd.DataFrame(fragments[:-1], columns = ["Document"])
#         df["PMID"] = pmids
#         return df
        

=======
def get_result():
    query = input("Please enter a search string: ")
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    database = "pubmed"
    retmax = 200
    url = f"{base_url}esearch.fcgi?db={database}&term={query}&retmax={retmax}&usehistory=y"


    response = requests.get(url)

    # if response.status_code == 200:
    #     try: 
    #         print(response.json())
    #     except requests.exceptions.JSONDecodeError: 
    #         print("Empty response or invalid JSON format. Status code: ", response.status_code)
    # else: 
    #     print("Failed to retrieve search results.") 

    root = ET.fromstring(response.text)
    web_env = root.find('WebEnv').text
    query_key = root.find("QueryKey").text
    efetch_url = f"{base_url}efetch.fcgi?db={database}&query_key={query_key}&retmax={retmax}&WebEnv={web_env}&rettype=abstract&retmode=text"
    Response = requests.get(efetch_url)
    abstracts_data = Response.text
    num_abstracts = len(abstracts_data.split('\n'))
    # print("Number of abstracts printed", num_abstracts)
    print(abstracts_data)
>>>>>>> 8135ae4 (Second commit)
