import os, pickle, csv, random, nltk, re, sys, unicodedata

from textwrap import TextWrapper
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures as BAM
from itertools import chain
import ttp

def pretty_print_status(status):
    status_wrapper = TextWrapper(width=60, initial_indent=' ', subsequent_indent=' ')
    print status_wrapper.fill(status.text)
    print '\n %s %s via %s\n' % (status.author.screen_name, status.created_at, status.source)

# Save Classifier
def SaveClassifier(classifier, filename="BayesClassifier"):
    fModel = open('%s'%filename,"wb")
    pickle.dump(classifier, fModel,1)
    fModel.close()
    os.system("gzip %s"%filename)

# Load Classifier   
def LoadClassifier(filename="BayesClassifier.pkl"):
    os.system("gunzip %s.gz"%filename)
    fModel = open('%s'%filename,"rb")
    classifier = pickle.load(fModel)
    fModel.close()
    os.system("gzip %s"%filename)
    return classifier 

def process_string(string):
    string = re.compile(r"\b\w\w+\b", re.U).findall(string.lower())
    return string

def word_features(words, score_fn=BAM.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict((bg, True) for bg in chain(words, bigrams))

def process_tweet(string):
    string = ttp.URL_REGEX.sub("", string)
    string = ttp.HASHTAG_REGEX.sub("", string)
    #string = ttp.REPLY_REGEX.sub("", string)
    string = ttp.USERNAME_REGEX.sub("", string)
    string = ttp.LIST_REGEX.sub("", string)
    string = string.replace("&quot;", "").replace("&lt;", "").replace("&gt;", "")
    return string