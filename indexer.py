import json, os, re, sys
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
from Posting import Posting

def default(obj):
    '''Encoder object to serialize Postings class as a JSON object'''
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def indexer():
    '''Read through JSON file, create docID, parse content with listed encoding, tokenize,
        stemming and other language processing, add doc as postings to inverted index (dictionary) '''
    main_index = defaultdict(dict)
    url_index = dict()
    docID = 0

    # using Porter2 stemmer to stem all english words except stop words
    stemmer = SnowballStemmer("english", ignore_stopwords=True)

    # changing into the DEV directory and opening it
    os.chdir("../DEV")
    for dir in os.listdir():
        if dir != '.DS_Store':
            print(f'Directory {dir} started')
            
            # opening the subdirectories in dev directory
            for file in os.listdir(dir):
                # file_index = defaultdict(int)
                
                # opening each file in subdirectories and parsing data
                if os.path.splitext(file)[1] == '.json':
                    with open(dir + '/' + file) as f:

                        # try/except allows us to view any errors that may occur and continue the code
                        try:
                            data = json.load(f)
                        except Exception as e:
                            print(f"Directory: {dir}, File: {file}")
                            print(f"Error: {e}")    # prints the type of error displayed
                            continue

                        # using BeautifulSoup to parse data
                        soup = BeautifulSoup(data['content'].encode(data['encoding']), 'lxml', from_encoding = data['encoding'])
                        tokens = word_tokenize(soup.get_text())
                    
                        # tokenizing alphanumerically
                        for token in tokens:
                            alphanum = re.sub(r'[^a-zA-Z0-9]', '', token)
                            
                            # only allowing alphanumeric characters to be stemmed
                            if len(alphanum) > 0:
                                stem = stemmer.stem(alphanum)
                                
                                # print(f'Token: {token}, Stem: {stem}')
                            
                                # file_index[stem] += 1
                                
                                # creating a Posting object to easily access docID and frequencies of tokens
                                # & putting the Posting objects into the main_index
                                if docID not in main_index[stem]:
                                    main_index[stem][docID] = Posting()
                                else:
                                    main_index[stem][docID].increment_freq()
                
        
                        # adding docIDs, frequencies, and URLs to dict and defaultdict
                        # for stem, freq in file_index.items():
                        #     main_index[stem].append((docID, freq))
                                    
                        url_index[docID] = data['url']
                            
                        docID += 1

            print(f'Directory {dir} done\n')
            # break

    # ensuring main_index.json gets dumped in inverted-index-m1 directory instead of DEV 
    os.chdir("../inverted-index-m1")
    
    # dumping main_index into a json
    with open("main_index.json", 'w') as f:
        json.dump(main_index, f, default=default)
        print("File index made")
        
    print(f"Number of documents: {docID + 1}")
    print(f"Number of tokens: {len(main_index)}")
    print(f"Size of index: {sys.getsizeof(main_index)}")

    # print('main index:')
    # print(main_index)
    # print('url index')
    # print(url_index)  
    
if __name__ == "__main__":
    indexer()