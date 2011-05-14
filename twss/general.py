from textwrap import TextWrapper
import os, pickle

def pretty_print_status(status):
    status_wrapper = TextWrapper(width=60, initial_indent=' ', subsequent_indent=' ')
    print status_wrapper.fill(status.text)
    print '\n %s %s via %s\n' % (status.author.screen_name, status.created_at, status.source)

# Save Classifier
def SaveClassifier(classifier, filename="BayesClassifier"):
    fModel = open('%s.pkl'%filename,"wb")
    pickle.dump(classifier, fModel,1)
    fModel.close()
    os.system("gzip %s.pkl"%filename)

# Load Classifier   
def LoadClassifier(filename="BayesClassifier"):
    os.system("gunzip %s.pkl.gz"%filename)
    fModel = open('%s.pkl'%filename,"rb")
    classifier = pickle.load(fModel)
    fModel.close()
    os.system("gzip %s.pkl"%filename)
    return classifier 

def process_string(string):
    string = re.compile(r"\b\w\w+\b", re.U).findall(string)
    return string

def word_features(words, score_fn=BAM.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict((bg, True) for bg in chain(words, bigrams))
