import threading 
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
        self.count = 0

    def on_data(self, data):
        print "ola"
        tweet = json.loads(data)
        auxDB = self.db.LEARNING
        if 'text' in tweet:
            texto = tweet['text'].encode('ascii','replace')
            auxDB.online.insert_one({'tweet':texto})
        self.count+=1
        if self.count < 100:
            return True
        else:
            return False

    def on_error(self,status_code):
        print error
        return False


#First class to initiate the Learning
#Doesnt use storm topology's 
#Given one tracker will start the feed taking 100 tweets
#All tweets are inserted in DB = LEARNING Collection = ONLINE
#The service will be responsable for insert data in the right topics
class Learning():
    def __init__(self,tracker):
        self.tracker = tracker
        self.feed= TwitterFeed
        #self.start()
        

    def start(self):
        t = threading.Thread(target=self.feed , args=(self.tracker,))
        print("start")
        t.start()
        print("waiting")
        t.join()
        print("end")
        return True
        
        
    def stop(self):
        self.feed.close()

#ola = Learning("donald")
#ola.start()
