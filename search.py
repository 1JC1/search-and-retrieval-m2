def process_query(query: str):
    # add stopword removal / recognition
    tokens_to_search = set()
    
    for token in query.split():
        alphanum = re.sub(r'[^a-zA-Z0-9]', '', token)
        
        if len(alphanum) > 0:
            stem = stemmer.stem(alphanum)
            tokens_to_search.add(stem)
    
    return tokens_to_search

def search(tokens: lst[str]):
    pass
