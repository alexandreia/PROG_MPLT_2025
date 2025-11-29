import nltk
from collections import defaultdict
from math import log2
import sys, time


def get_lines(file_path):
    with open(file_path, 'r') as f: 
        text = f.read()
    return text


def get_unigrams(list_sentences):
    unigram_freq = defaultdict(int) # dictionary with default value 0

    for sentence in list_sentences:
        #tokenize sentences into words
        #add start and end tokens
        tokens = ['<s>'] + nltk.word_tokenize(sentence) + ['<e>']
        #count frequencies
        for token in tokens:
            unigram_freq[token] += 1
    return unigram_freq


def get_bigrams(lst_sent):
    bigram_freq = defaultdict(int)
    for sentence in lst_sent:
        #tokenize sentences into words
        #add start and end tokens
        tokens = ['<s>'] + nltk.word_tokenize(sentence) + ['<e>']
        for index in range(len(tokens)-1):
            #range(len(tokens) - 1) stops at the second-to-last index, so tokens[i + 1] is always valid.
            pair = (tokens[index], tokens[index + 1])
            bigram_freq[pair] += 1 #to use get: bigram_freq[pair] = bigram_freq.get(pair,0) +1  if not usng defaultdict . dict.get(key, 0) returns the current count if it exists, otherwise 0. value = bigram_freq.get(key, default_value)
    return bigram_freq


def get_surprisal(prob):
    if prob <= 0:
        return None 
    return -log2(prob)


    
def get_bigram_surprisal(unigram_freq_dict, bigram_freq_dict):
    bigram_surprisal = {} #By using float, we ensure the dictionary can safely store numbers like 0.75, 3.3219, etc. results are fractional/real numbers
    for bigram, bigram_count in bigram_freq_dict.items():
        w1 = bigram[0]
        unigram_count = unigram_freq_dict.get(w1)
        # Only compute if unigram_count > 0 (should always be true)
        #if unigram_count > 0:   ### DO NOT NEED THE IF
            # Equation (1): conditional probability
        prob = bigram_count / unigram_count
            # Equation (2): surprisal = -log2(p)
        surp = get_surprisal(prob)
        bigram_surprisal[bigram] = surp
        # If unigram count = 0, skip (bigram shouldn’t exist)
        #use the unigram dictionary to look up the first word’s frequency when calculating probabilities for each bigram. use the unigram counts to normalize the bigram counts.
    return bigram_surprisal


def main():
    if len(sys.argv) < 2: #check if th file path was provided
        print("Did you forget to add the corpus file?")
        sys.exit(1)
    file_path = sys.argv[1]
    #read traning file
    train_text = get_lines(file_path) #read file contents

    #tokenize nto sentences 
    train_sentences = nltk.sent_tokenize(train_text) #tokenize into sentences
    
    #get unigrams and bigrams
    unigram_freq = get_unigrams(train_sentences) #get unigrams frequency
    bigram_freq = get_bigrams(train_sentences)
    bigram_surprisal = get_bigram_surprisal(unigram_freq, bigram_freq)
    bi_surp = get_bigram_surprisal(unigram_freq, bigram_freq)
    print(bi_surp.get(('this','is')))
    print(bi_surp.get(('this','issue')))
    print(bi_surp.get(('and','why')))
    print(bi_surp.get(('which','can')))


    
if __name__ == "__main__":
    main()


