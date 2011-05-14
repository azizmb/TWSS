import time
from getpass import getpass

import tweepy
from tweepy import Status, Cursor
from tweepy.utils import import_simplejson
json = import_simplejson()
import csv
import webbrowser

class StreamWatcherListener(tweepy.StreamListener):
    
    def __init__(self, *args, **kwargs):
        filename = kwargs.get("filename", "general.csv")
        self.c = csv.writer(open('general.csv', 'wb'))
        super(StreamWatcherListener, self).__init__(*args, **kwargs)
        
    def on_data(self, data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """

        if 'in_reply_to_status_id' in data and '"lang":"en"' in data:
            status = Status.parse(self.api, json.loads(data))
            if self.on_status(status) is False:
                return False
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False

    def on_status(self, status):
        try:
            text = status.text
            self.c.writerow(["general", text])
        except Exception as e:
            print e
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def main():
    #username = raw_input('Twitter username: ')
    #password = getpass('Twitter password: ')
    username = "azizbookwala"
    password = "cool435toad"
    stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)
    stream.sample()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'