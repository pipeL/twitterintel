import thread
import tweepy
import nltk
import json
import pymongo


class TwitterFeed():
    def __init__(self,track):
        consumer_key = "eaFmBSxUveRJfmyZYeabti9Q9"
        consumer_secret= "ADf76fi3O1lKMzBxWnjqf93l3GHv28uar3bkblkvyBrAyoA23i"
        acess_token= "702208758362087425-HZiyl1x7Bh98cQa1WLBDYylyu10Bpl7"
        acess_token_secret= "IiNOTfgE3tEZvW2HDQhRKPMoOLU43NXJCXk8maj51SdAT"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(acess_token,acess_token_secret)
        self.stream = tweepy.Stream(auth, TwitterListener())
        self.stream.filter(track=[track])
        
    
    def close(self):
        self.stream.disconnect()
        return True

class TwitterListener(tweepy.StreamListener):
    def __init__(self):
        self.stop=set(nltk.corpus.stopwords.words('english'))
        self.stop.update(['http','https','rt'])
        self.db = pymongo.MongoClient()

    def on_data(self, data):
        tweet = json.loads(data)
        auxDB = self.db.LEARNING
        count = 0
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nTWEETS:\n')
        print('Good(g) Bad(b) SPAM(s):\n')
        if 'text' in tweet:
            texto = tweet.encode('ascii','replace')
            auxDB.online.insert_one({'tweet':texto})
            count+=1
            if count == 31:
                return False
        return True

class Learning():
    def __init__(self,tracker):
        self.tracker = tracker
        self.feed= TwitterFeed
        #self.start()
        

    def start(self):
        try:
            self.feed(self.tracker)
        except:
            pass
        return 
        
        
    def stop(self):
        self.feed.close()
