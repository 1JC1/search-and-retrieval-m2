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

def intersect(list_1, list_2, postings, first = False):
    result_docIDs = []
    new_postings = defaultdict()
    p1 = 0
    p2 = 0
    
    while p1 < len(list_1) and p2 < len(list_2):
        if list_1[p1] == list_2[p2]:
            shared_docID = list_1[p1].get_docID()
            result_docIDs.append(shared_docID)
            if first:
                postings[shared_docID].append(list_1[p1])
            postings[shared_docID].append(list_2[p2])
            p1 += 1
            p2 += 1
        elif list_1[p1] < list_2[p2]:
            p1 += 1
        else:
            p2 += 1
            
    for id in result_docIDs:
        new_postings[id] = postings[id]
    
    return (result_docIDs, new_postings)



def simple_rank(postings):
    rel_score = defaultdict(int)

    for id in postings.keys():
        for post in postings[id]:
            rel_score[id] += post.get_freq()

    return sorted(rel_score.keys(), key=lambda x : rel_score[x], reverse=True)[0:5] 
    

    
def search(tokens: set[str], index):
    token_list = [t for t in tokens if t in index]
    token_list.sort(key=lambda t: len(index[t]))
    
    result_list = []
    
    if len(token_list) > 1:
        posting_dict = defaultdict(list)
        result_list, posting_dict = intersect(index[token_list[0]], index[token_list[1]], posting_dict, True)
        
        for i in range(2,len(token_list)):
            result_list, posting_dict = intersect(result_list, index[token_list[i]], posting_dict)
        
    elif len(token_list) == 1:
        result_list = index[token_list[0]]

    return simple_rank(posting_dict)

 
 
if __name__ == "__main__":
    token_index, url_index = indexer()
    
    while True:
        query = input("What would you like to search? Press Q to quit.\n")
        
        if query.lower() == 'q':
            break
        
        result_list = search(process_query(query), token_index)
        
        print(f"Searching for query {query}... ")
        for count, id in enumerate(result_list, start=1):
            print(f"{count} | {url_index[id]:100}")
        
        print()
    