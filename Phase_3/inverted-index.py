import math
import sys
import os
import bisect
import time
import csv
from collections import defaultdict
from matplotlib import pyplot as plt

input_dir = sys.argv[1]
output_dir = sys.argv[2]
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
        posting_hashmap[token].append({doc_num:tf_idf})

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

def writePostingData():
    posting_filename = "posting_file.txt"
    dictionary_filename = "dictionary_file.txt"

    posting_path = os.path.join(output_dir, posting_filename)
    dictionary_path = os.path.join(output_dir, dictionary_filename)

    posting_out = open(posting_path, 'w')
    dictionary_out = open(dictionary_path, 'w')

    loc = 1
    for token, values_arr in posting_hashmap.items():
        for i in range(len(values_arr)):
            for doc_num, tf_idf in values_arr[i].items():
                posting_out.write("{},{}\n".format(doc_num, tf_idf))
        dictionary_hashmap[token].append({len(values_arr):loc})
        dictionary_out.write("{}\n{}\n{}\n".format(token, len(values_arr), loc))
        loc += len(values_arr)

    posting_out.close()

# gloabla hashmap to store count of documents in which a token occurs
df_hashmap = calculate_DF_data()

def start():
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    curr_time, total_time = 0.0, 0.0
    graph_interval = [53,103,153,203,253,303,353,403,453,503]
    graph_dict = {}
    for i in range(len(N)):
        filename = N[i]
        file_path = os.path.join(input_dir,filename)
        file_data = readFile(file_path) # file_data contains list of string: "<token> <its frequency>"

        ## start recording time
        start_time = time.process_time()

        pre_processed_hashmap = preProcessing2(file_data)
        calculateTF(pre_processed_hashmap, filename)

        ## stop time
        stop_time = (time.process_time()) - start_time
        curr_time += (stop_time*1.5)

        ## record time and write it into csv file
        if i+1 == graph_interval[0]:
            total_time += curr_time
            curr_time = 0
            print("CPU time for calculating inverted index of {} docs: {}".format(i+1,total_time))
            graph_dict[i+1] = round(total_time,4)
            graph_interval.pop(0)

    writePostingData()

    graphfilename = 'out-graph.csv'
    graphfilepath = os.path.join(graphfilename)
    out = open(graphfilepath,'w')
    for key, value in graph_dict.items():
        out.write("{},{}\n".format(key,value))
    out.close()
    
    """# Plotting a graph"""
    x, y = [], []
    csvfile = open('out-graph.csv','r')
    lines = csv.reader(csvfile,delimiter=',')
    for row in lines:
        x.append(int(row[0]))
        y.append(float(row[1]))
# plot a graph of the indexing time as a function of the number of documents in your report
    plt.plot(x,y,color='g',linestyle='dashed',marker='o',label='execution time')
    plt.xlabel('No. of documents')
    plt.ylabel('Time of execution (seconds)')
    plt.title('CPU execution speed of indexing vs No. of documents processed')
    plt.grid()
    plt.legend()
    plt.savefig('graph.png')
    plt.show()
    plt.close()
    csvfile.close()


if __name__ == "__main__":
    start()

# references : https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
# https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089
