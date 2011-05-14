from getpass import getpass

import tweepy
from tweepy import Status, Cursor, Stream
from tweepy.utils import import_simplejson
json = import_simplejson()

from listners import InReplyListener, TWSSBuildClassifierListner
from general import process_tweet

def interactive(username=None, password=None, filenames=None):
    if not username:
        username = raw_input('Username: ').strip()
    if not password:
        password = getpass("Password: ").strip()
    s = Stream(username, password, TWSSBuildClassifierListner())
    s.sample()
    
def from_stream(username=None, password=None, track=[], filename="twitter_twss.csv", limit=None):
    if not username:
        username = raw_input('Username: ').strip()
    if not password:
        password = getpass("Password: ").strip()
    if not len(track):
        track = ["#twss", "#thatswhatshesaid", '"thats what she said"']
    stream = tweepy.Stream(username, password, InReplyListener(csv_file=filename, tweet_processor=process_tweet))
    stream.filter(track=track)
    

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
            status = api.get_status(api.get_status(item.id).in_reply_to_status_id)
            c.writerow([process_tweet(status.text),])
            
        except Exception as e:
            print e
