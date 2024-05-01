import requests 
import json
import xml.etree.ElementTree as ET
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
