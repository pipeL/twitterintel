from kafka import KafkaConsumer
from kafka import KafkaProducer
import thread
import tweepy
import nltk
import json
import math
import threading
import sys
import time
import pymongo
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment 


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
        self.stream = tweepy.Stream(auth, TwitterListener(stop,user),timeout=60)
        self.stream.filter(track=[track])
        
    
    def close(self):
        self.stream.disconnect()
        return True

class TwitterListener(tweepy.StreamListener):
    def __init__(self,stop,user):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.instanttopic = 'instanttopic'
        self.user = str(user)
        self.numstop = int(stop)

    def on_data(self, data):
        fil = open("meu.txt","a")
        stop=set(nltk.corpus.stopwords.words('english'))
        stop.update(['http','https','rt'])
        tweet = json.loads(data)
        if 'text' in tweet:
            texto = tweet['text'].encode('ascii','ignore')
            self.numstop -=1
            texto = self.user+'-'+texto
            self.producer.send(self.instanttopic,texto)
            saveTweet('pos',tweet,self.user)
            saveLocation('pos',tweet,self.user)

            vs = vaderSentiment(str(texto))
            contagemneg= vs['neg']
            contagempos= vs['pos']
            contagemspam=vs['neu']
            filo= open("vader.txt",'a')
            if self.numstop == 0:
                return False
        return True

            


def saveLocation(tipo,tweet,user):
    db = pymongo.MongoClient()
    board = 'BOARD'+user
    if tweet['coordinates']:
        if tipo == 'pos':
            db[board].goodlocation.insert_one({"tweet":tweet['text'] , "created_at":tweet['created_at'] , "location": tweet['coordinates']})
        else:
            db[board].badlocation.insert_one({"tweet":tweet['text'] , "created_at":tweet['created_at'] , "location": tweet['coordinates']})
    
def saveTweet(tipo, tweet,user):
    db = pymongo.MongoClient()
    board = 'BOARD'+user
    id_str= tweet['user']['id']
    n_followers=tweet['user']['followers_count']
    location= tweet['user']['location']
    name = tweet['user']['name']
    friends_count = tweet['user']['friends_count']
    timenow = time.strftime("%H:%M")
    
    if(tipo == 'pos'):
        db[board].goodcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = db[board].goodcounter.find_one()
        auxcount = auxcount["count"]
        db[board].goodinfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count , "time": timenow})

    elif(tipo == 'neg'):
        board.badcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.badcounter.find_one()
        auxcount = auxcount["count"]
        board.badinfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count , "time": timenow})

    elif(tipo == 'spam'):
        board.spamcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = db[board].spamcounter.find_one()
        auxcount = auxcount["count"]
        board.spaminfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count, "time":timenow})


class StopThread(StopIteration): pass

threading.SystemExit = SystemExit, StopThread

class Thread2(threading.Thread):

    def stop(self):
        self.__stop = True

    def _bootstrap(self):
        if threading._trace_hook is not None:
            raise ValueError('Cannot run thread with tracing!')
        self.__stop = False
        sys.settrace(self.__trace)
        super()._bootstrap()

    def __trace(self, frame, event, arg):
        if self.__stop:
            raise StopThread()
        return self.__trace

class InstantFeed():
    def __init__(self,tracker,stop,user):
        self.tracker = tracker
        self.feed= TwitterFeed
        self.t = Thread2(target=self.feed,args=(self.tracker,stop,user,))
        

    def start(self):
        self.t.start()
        self.t.join()
        return True
        
    def stop(self):
        self.t.stop()
        
