import json, os, re, sys, heapq
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from Posting import Posting
from indexer import indexer

def process_query(query: str):
    # add stopword removal / recognition
    tokens_to_search = set()
    
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    
    for token in word_tokenize(query):
        alphanum = re.sub(r'[^a-zA-Z0-9]', '', token)
        
        if len(alphanum) > 0:
            stem = stemmer.stem(alphanum)
            tokens_to_search.add(stem)
    
    return tokens_to_search

def search(tokens: set(str), index):
    token_list = list(tokens).sort(key=lambda t: )
    
    for token in tokens:
        index[token]
        

if __name__ == "__main__":
    main_index = indexer()
    
