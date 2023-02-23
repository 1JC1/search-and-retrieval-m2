import json, os, re, sys, heapq
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from Posting import Posting
from indexer import indexer

main_index = dict()

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

def search(tokens: set(str)):
    token_list = list(tokens).sort(key=lambda t: len(main_index[t]))

def intersect(list_1, list_2):
    answer = []
    p1 = 0
    p2 = 0
    
    while p1 < len(list_1) and p2 < len(list_2):
        if list_1[p1].get_docID() == list_2[p2].get_docID():
            answer.append(list_1[p1].get_docID())
            p1 += 1
            p2 += 1
        elif list_1[p1].get_docID() < list_2[p2].get_docID():
            p1 += 1
        else:
            p2 += 1
    
    return answer
    
        

if __name__ == "__main__":
    main_index = indexer()
    
