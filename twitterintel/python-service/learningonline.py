import threading 
import tweepy
import nltk
import json
import pymongo


class TwitterFeed():
    def __init__(self,track,stop,user):
        db = pymongo.MongoClient()
        data = db.LOGIN.login.find_one({'_id':int(user)})
        consumer_key = data['consumer_key']
        consumer_secret= data['consumer_secret']
        access_token= data['access_token']
        access_token_secret= data['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        self.stream = tweepy.Stream(auth, TwitterListener(stop,user),timeout=30)
        self.stream.filter(track=[track])
        
    
    def close(self):
        self.stream.disconnect()
        return True

class TwitterListener(tweepy.StreamListener):
    def __init__(self,number,user):
        self.stop=set(nltk.corpus.stopwords.words('english'))
        self.stop.update(['http','https','rt'])
        self.db = pymongo.MongoClient()
        self.aux = 'LEARNING'+user
        #print 'ola'
        self.count = int(number)

    def on_data(self, data):
        #print 'hj'
        tweet = json.loads(data)
        auxDB = self.db[self.aux]
        if 'text' in tweet:
            texto = tweet['text'].encode('ascii','ignore')
            auxDB.online.insert_one({'tweet':texto})
        self.count-=1
        if self.count > 0:
            return True
        else:
            return False
    def on_error(self,error):
        print error


#First class to initiate the Learning
#Doesnt use storm topology's 
#Given one tracker will start the feed taking 100 tweets
#All tweets are inserted in DB = LEARNING Collection = ONLINE
#The service will be responsable for insert data in the right topics
class Learning():
    def __init__(self,tracker,number,user):
        self.tracker = tracker
        self.number = number
        self.user= user
        self.feed= TwitterFeed
        #self.start()
        

    def start(self):
        t = threading.Thread(target=self.feed , args=(self.tracker,self.number,self.user))
        #print("start")
        t.start()
        #print("waiting")
        t.join()
        #print("end")
        return True
        
        
    def stop(self):
        self.feed.close()

#ola = Learning("donald")
#ola.start()
