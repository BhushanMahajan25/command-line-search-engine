# -*- coding: utf-8 -*-

# Name: Bhushan Mahajan
# Email: m302@umbc.edu
# Campus ID: MM65493

"""# HTML2TEXT"""

import re
import os
import sys
import time
import html2text
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from gensim.utils import tokenize

input_dir_path = sys.argv[1]
output_dir_path1 = sys.argv[2]

html_parser = html2text.HTML2Text() #reference: https://pypi.org/project/html2text/
html_parser.ignore_links = True 
html_parser.ignore_images = True

def clean(string): # refence: https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
  # return re.sub(r"[^a-zA-Z]","",string)
  return re.sub(r"[\s\n\r\t\f\_]",'',string)

def generate_output_file(filename,output_dir_path,token_dict):
  filename = 'out' + '-' + os.path.splitext(filename)[0]+'.txt'
  #print('output filename: ', filename)
  filepath = filename
  if output_dir_path:
    filepath = os.path.join(output_dir_path, filename)
  out = open(filepath,'w')
  for key, value in token_dict.items():
    out.write("{} {}\n".format(key,value))
  out.close()

token_dict = defaultdict()  # this is global dict for storing all tokens in one dict for solution 2 & 3

file_list = os.listdir(input_dir_path)

"""## Generating graph for docs num: 53, 103, 153, 203, 253, 303, 353, 403, 453, 503"""

#total_time, curr_time are in seconds
def tokenize_words(graph_interval, graph_dict, total_time=0.0, curr_time=0.0):
  # refernce: https://docs.python.org/3/library/os.html
  for i in range(len(file_list)):
    filename = file_list[i]
    filepath = os.path.join(input_dir_path, filename)
    # checking if it is a file
    if not os.path.isfile(filepath):
      print("{} invalid file or file does not exist".format(filepath))
    else:
      # print("parsing the file ", filepath)
      local_dict = defaultdict()
      html_file = open(filepath,'r',encoding="unicode_escape") #reference: https://docs.python.org/2.4/lib/standard-encodings.html 
      html = html_file.read()
      html_file.close()
      # print(html_parser.handle(html).split())

      ## start recording time
      start_time = time.process_time()

      words = html_parser.handle(html)
      # word_list = words.split() # tokenizer used: split()
      tokens = tokenize(words)  # tokenizer used: genism
      word_list = list(tokens)
      for word in word_list:
        ret = clean(word)
        # ret = word
        if ret:
          ret = ret.lower()
          token_dict[ret] = 1 + token_dict.get(ret,0)  # this is global dict for storing all tokens in one dict.
          local_dict[ret] = 1 + local_dict.get(ret,0) # this stores op of each ip file for solution-1
      # print(local_dict)

      ## stop time
      stop_time = (time.process_time()) - start_time
      curr_time += stop_time

      generate_output_file(filename,output_dir_path1,local_dict)
      
      ## record time and write it into csv file
      if i+1 == graph_interval[0]:
        total_time += curr_time
        curr_time = 0
        print("CPU time for tokenizing {} docs: {}".format(i+1,total_time))
        graph_dict[i+1] = round(total_time,4)
        graph_interval.pop(0)
  #print(graph_dict)

grah_interval = [53,103,153,203,253,303,353,403,453,503]
graph_dict = {}
tokenize_words(grah_interval,graph_dict)

graphfilename = 'out-graph.csv'
#print('output filename: ', filename)
graphfilepath = os.path.join(graphfilename)
out = open(graphfilepath,'w')
for key, value in graph_dict.items():
  out.write("{},{}\n".format(key,value))
out.close()

# print(token_dict)

"""# Solution-2: 
A file of all tokens and their frequencies sorted by token

"""
# solution-2
new_dict = dict(sorted(token_dict.items(),key=lambda x:x[0]))
generate_output_file('sol-2','',new_dict)

"""# Solution-3:
a file of all tokens and their frequencies sorted by frequency
"""
# solution-3
new_dict = dict(sorted(token_dict.items(),key=lambda x:x[1]))
generate_output_file('sol-3','',new_dict)

"""# Plotting a graph"""

x, y = [], []
csvfile = open('out-graph.csv','r')
lines = csv.reader(csvfile,delimiter=',')
for row in lines:
  x.append(int(row[0]))
  y.append(float(row[1]))

plt.plot(x,y,color='g',linestyle='dashed',marker='o',label='execution time')
plt.xlabel('No. of documents tokenized')
plt.ylabel('Time of execution (seconds)')
plt.title('No. of documents processed vs CPU execution speed')
plt.grid()
plt.legend()
plt.savefig('graph.png')
plt.show()
plt.close()
csvfile.close()

