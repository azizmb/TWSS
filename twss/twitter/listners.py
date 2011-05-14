import csv, os
import tweepy

from general import pretty_print_status, LoadClassifier, process_string, process_tweet, word_features

class TWSSListner(tweepy.StreamListener):
    def __init__(self, csv_file=None, classifier="twss_classifier.pkl", **kwargs):
        if csv_file:
            self.c = csv.writer(open(csv_file, 'wb'))
        else:
            self.c = None
        classifier = os.path.abspath(classifier)
        self.classifier = LoadClassifier(filename=classifier)
        super(TWSSListner, self).__init__(**kwargs)
    
    def on_status(self, status):
        try:
            print status.text
            cls = self.classifier.classify(word_features(process_string(process_tweet(status.text))))
            if self.c:
                self.c.writerow([cls, status.text, process_tweet(status.text)])
        except Exception as e:
            print e
            
class TWSSBuildClassifierListner(tweepy.StreamListener):
    def __init__(self, csv_files=("general.csv", "twss.csv"), classifier="twss_classifier.pkl", **kwargs):
        classifier = os.path.abspath(classifier)
        self.classifier = LoadClassifier(filename=classifier)
        
        self.gen_writer = csv.writer(open(csv_files[0], "wb"))
        self.twss_writer = csv.writer(open(csv_files[1], "wb"))
        
        super(TWSSBuildClassifierListner, self).__init__(**kwargs)
    
    def on_status(self, status):
        try:
            print status.text
            cls = raw_input("TWSS? ")
            if cls.lower() == "y":
                writer = self.twss_writer
            else:
                writer = self.gen_writer
            writer.writerow([process_tweet(status.text)])
        except Exception as e:
            print e
        
class InReplyListener(tweepy.StreamListener):
    def __init__(self, csv_file=None, tweet_processor=None, **kwargs):
        self.tweet_processor = tweet_processor
        if csv:
            self.c = csv.writer(open(csv_file, 'wb'))
        else:
            self.c = None
        super(InReplyListener, self).__init__()
        
    def on_status(self, status):
        try:
            if status.in_reply_to_status_id:
                original = self.api.get_status(status.in_reply_to_status_id)
                text = original.text
                pretty_print_status(orignal)
                if self.tweet_processor:
                    text = self.tweet_processor(text)
                if self.c:
                    self.c.writerow([text, ])
        except Exception as e:
            print e
            pass
