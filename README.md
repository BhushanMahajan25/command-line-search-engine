# Search Engine from scratch
The project consists of five phases of building a basic search engine from scratch.

## Phase 1 : Tokenization
1. Parsing the HTML document using BeautifulSoap
2. Cleaning the parsed string using RegEx
3. Tokenizing the words from the cleaned document using NLTK

## Phase 2 : Term Weighting
1. Creating a global corpus dictionary: HashMap is created to calculate the number of occurrences of a token in all the documents.
2. Pre-processing each file: Removing the stopwords and words with length 1.
3. Calculating all the required values: 
  - Term frequency = no. of occurrences token/total no. of tokens in the document
  - Document frequency = no. of occurrences of a token in all 500 documents
  - Inverse document frequency = log(no. of documents/ document frequency)
  - Weight of token = term frequency * inverse document frequency

## Phase 3 : Indexing
1. All the steps from phase 2 are repeated.
2. Writing the Posting file: HashMap is then passed to a function which writes the files with the number of documents in which that token has occurred and its tfidf.
3. Writing the Dictionary file: HashMap is passed to another function which writes the token, number of occurrences of that token in all documents and sum of the frequency of previous token and its occurrence


## Phase 4 : Retrieval

