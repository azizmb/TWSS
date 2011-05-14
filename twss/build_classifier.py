import csv, random, nltk, re, sys, unicodedata
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures as BAM
from itertools import chain

from general import SaveClassifier


def main(argv):
    
    general_file = 'general.csv'
    twss_file = 'twss.csv'
        
    if len(argv):
        general_file = argv[0]
        twss_file = argv[1]
    
    print "Loading general corpus..."
    reader = csv.reader(open(general_file, 'rb'))
    general = [(process_string(l[0]), "general") for l in reader]
    
    print "Loading twss corpus..."
    reader = csv.reader(open('twss.csv', 'rb'))
    twss = [(process_string(l[0]), "twss") for l in reader]
    
    m = min((len(general), len(twss)))
    
    print "Compiling corpus..."
    corpus = twss[:m] + general[:m]
    random.shuffle(corpus)
    
    feature_set = [(word_features(l), g) for (l, g) in corpus]
    
    print "Building classifier..."
    classifier = nltk.NaiveBayesClassifier.train(feature_set)
    
    print "Saving classifier..."
    SaveClassifier("twss_classifier")
    
    
if __name__ == '__main__':
    main(sys.argv[1:])
