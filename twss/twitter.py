import time
from getpass import getpass

import tweepy
from tweepy import Status, Cursor
from tweepy.utils import import_simplejson
json = import_simplejson()
import csv
import webbrowser
from tweepy import Cursor
from general import process_tweet

class StreamWatcherListener(tweepy.StreamListener):
    
    def __init__(self, *args, **kwargs):
        filename = kwargs.get("filename", "general.csv")
        self.c = csv.writer(open('general.csv', 'wb'))
        super(StreamWatcherListener, self).__init__(*args, **kwargs)
        
    def on_status(self, status):
        try:
            text = status.text
            print text
            #self.c.writerow()
        except Exception as e:
            print e
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'
        
def from_stream():
    pass

def from_search(consumer_key=None, consumer_secret=None, track=[], filename="twitter_twss.csv"):
    if not consumer_key:
        consumer_key = raw_input('Consumer key: ').strip()
    if not consumer_secret:
        consumer_key = raw_input('Consumer secret: ').strip()
    if not len(track):
        track = ["#twss", "#thatswhatshesaid", '"thats what she said"']
        
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    
    api = tweepy.API(auth)
    
    c = csv.writer(open(filename, "wb"))
    
    for item in Cursor(api.search, q=' OR '.join(track_list)).items():
        try:
            print "Reply: %s"%item.text
            status = api.get_status(api.get_status(item.id).in_reply_to_status_id)
            print "Orignal: %s"%status.text
            c.writerow([process_tweet(status.text),])
            
        except Exception as e:
            print e
                    

import sys
if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print '\nGoodbye!'