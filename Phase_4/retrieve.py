import math
import re
import sys
import os
import bisect
from collections import defaultdict

input_dir = 'files'
stop_list_filename = 'stoplist.txt'
N = os.listdir(input_dir)   # count of corpus
posting_hashmap = defaultdict(list)
dictionary_hashmap = defaultdict(list)

def readFile(filename):
    file = open(filename, 'r')
    ret = file.read().splitlines()
    file.close()
    return ret

stop_words_list = readFile(stop_list_filename)

# searches a token in stop words list
def binarySearch(token):
    i = bisect.bisect_left(stop_words_list, token)
    return i if (i != len(stop_words_list) and stop_words_list[i] == token) else -1

# pre-processing on tokens in each document
def preProcessing2(file_data):
    pre_processed_hashmap = {}
    # remove remove stopwords, words that occur only once in the entire corpus, and words of length 1
    for i in range(len(file_data)):
        temp = file_data[i].split(" ")
        token, freq = temp[0], int(temp[1])

        if binarySearch(token) != -1 or len(token) == 1 or df_hashmap[token] == 1:
            continue
        pre_processed_hashmap[token] = freq
    return pre_processed_hashmap

# TF-IDF calculation
def calculateTF(pre_processed_hashmap, filename):
    # total tokens in d
    count_tokens_doc = len(pre_processed_hashmap.keys())
    doc_num = int(os.path.splitext(filename)[0].split("-")[1])
    for token, freq in pre_processed_hashmap.items():
        tf = freq / count_tokens_doc
        df = df_hashmap[token]
        n = len(N)
        idf = math.log(n/df)    
        tf_idf = tf * idf
        # posting_hashmap[token].append({doc_num:tf_idf})
        posting_hashmap[token].append({'doc_num':doc_num,'tf_idf':tf_idf})
        posting_hashmap[token].sort(key=lambda x: x['tf_idf'], reverse=True)


def calculate_DF_data():
    hm = {}
    for i in range(len(N)):
        filename = N[i]
        file_path = os.path.join(input_dir,filename)
        file_data = readFile(file_path) # file_data contains list of string: "<token> <its frequency>"
        for i in range(len(file_data)):
            temp = file_data[i].split(" ")
            hm[temp[0]] = 1 + hm.get(temp[0], 0)
    return hm

def writeDictionaryData():
    loc = 1
    for token, values_arr in posting_hashmap.items():
        dictionary_hashmap[token].append({len(values_arr):loc})
        loc += len(values_arr)

# gloabla hashmap to store count of documents in which a token occurs
df_hashmap = calculate_DF_data()

def searchKeywords(input_hashmap):
    for input_token in input_hashmap:
        if input_token in dictionary_hashmap:
            print(input_token,"\n")
            ll = posting_hashmap[input_token]
            size = len(ll) if len(ll) < 10 else 10
            for i in range(size):
                print("Document: {}.html  tf-idf: {}".format(ll[i]['doc_num'], ll[i]['tf_idf']))
        else:
            print("Keyword {} not found!".format(input_token))
        print("\n")

def start():
    for i in range(len(N)):
        filename = N[i]
        file_path = os.path.join(input_dir,filename)
        file_data = readFile(file_path) # file_data contains list of string: "<token> <its frequency>"

        pre_processed_hashmap = preProcessing2(file_data)
        calculateTF(pre_processed_hashmap, filename)

    writeDictionaryData()
    

def clean(string): # refence: https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
  return re.sub(r"[^a-zA-Z]","",string)
#   return re.sub(r"[\s\n\r\t\f\_]",'',string)

def preprocessInput(ip_arr):
    input_hashmap = {}
    for token in ip_arr:
        if token == "--wt": continue
        token = clean(token)
        if token:
            input_hashmap[token.lower()] = None
    return input_hashmap

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please specify keywords to search")
        sys.exit(0)
    input_hashmap = preprocessInput(sys.argv[1:])
    start()
    searchKeywords(input_hashmap)
