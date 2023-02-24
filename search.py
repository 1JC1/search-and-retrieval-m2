import json, os, re, sys, heapq
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from Posting import Posting
from indexer import indexer
from collections import defaultdict

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

def intersect(list_1, list_2):
    answer = set()
    p1 = 0
    p2 = 0
    
    while p1 < len(list_1) and p2 < len(list_2):
        if list_1[p1] == list_2[p2]:
            answer.add(list_1[p1])
            answer.add(list_1[p2])
            p1 += 1
            p2 += 1
        elif list_1[p1] < list_2[p2]:
            p1 += 1
        else:
            p2 += 1
    
    return answer


def simple_rank(result_list):
    rel_score = defaultdict(float)

    for posting in result_list:
        rel_score[posting.get_docID()] += posting.get_freq()

    return sorted(rel_score, key=lambda x : rel_score[x], reverse=True)[0:5] 
    

    
def search(tokens: set[str], index):
    token_list = [t for t in tokens if t in index]
    token_list.sort(key=lambda t: len(index[t]))
    
    result_list = []
    
    if len(token_list) > 1:
        result_list = intersect(index[token_list[0]], index[token_list[1]])
        
        for i in range(2,len(token_list)):
            result_list = intersect(result_list, index[token_list[i]])
        
    elif len(token_list) == 1:
        result_list = index[token_list[0]]

    return simple_rank(result_list)

 
if __name__ == "__main__":
    token_index, url_index = indexer()
    
    while True:
        query = input("What would you like to search? Press Q to quit.\n")
        
        if query.lower() == 'q':
            break
        
        result_list = search(process_query(query), token_index)
        
        print(f"Searching for query {query}... ")
        for count, result in enumerate(result_list, start=1):
            print(f"{count} | {url_index[result.get_docID()]:100} | {result.get_freq()}")
        
        print()
    