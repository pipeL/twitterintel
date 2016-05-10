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
    def __init__(self,bad,good,spam,track,stop,user):
        db = pymongo.MongoClient()
        data = db.LOGIN.login.find_one({'_id':int(user)})
        consumer_key = data['consumer_key']
        consumer_secret= data['consumer_secret']
        access_token= data['access_token']
        access_token_secret= data['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        self.stream = tweepy.Stream(auth, TwitterListener(bad,good,spam,stop,user,timeout=60))
        self.stream.filter(track=[track])
        
    
    def close(self):
        self.stream.disconnect()
        return True

class TwitterListener(tweepy.StreamListener):
    def __init__(self,bad,good,spam,stop,user):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.topicbad = 'badtopic'
        self.topicgood = 'goodtopic'
        self.topicspam= 'spamtopic'
        self.bad = bad
        self.good= good
        self.spam = spam
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
            tokens = nltk.word_tokenize(tweet['text'])
            (guessgood,guessbad) = help(self.bad,self.good,self.spam,tweet['text'])
            #print('RealTweet: ' + texto + '\n')
            if guessgood>guessbad: 
                #print('Positive: ' + texto + '\n')
                self.producer.send(self.topicgood,texto)
                saveTweet('pos',tweet,self.user)
                saveLocation('pos',tweet,self.user)
                fil.write('POSITIVE:\n' + '\nTotal bad:' +  str(guessbad) + '\nTotal good:' +  str(guessgood) + '\n' + str(texto) + '\n\n\n')
                fil.close()
            else:
                #print('Negative: ' + texto + '\n')
                self.producer.send(self.topicbad,texto)
                saveTweet('neg',tweet,self.user)
                saveLocation('neg',tweet,self.user)
                fil.write('NEGATIVE:\n' +'\nTotal good:' +  str(guessgood) +  '\nTotal bad:' + str(guessbad) + '\n' + str(texto) + '\n\n\n')
                fil.close()

            vs = vaderSentiment(str(texto))
            contagemneg= vs['neg']
            contagempos= vs['pos']
            contagemspam=vs['neu']
            filo= open("vader.txt",'a')
            filo.write('Neg:' + str(contagemneg) + '\nPos:' + str(contagempos) + '\nNeutro:' + str(contagemspam) + '\nTotal guess:' + str(guessbad) + 'guessgood\n' + str(guessgood) + ' ' + str(texto) + '\n\n\n')
            filo.close()
            #elif (guess=='spam'): #and guess2=='spam' and guess3=='spam'):
                #print('Spam: ' + texto + '\n')
                #self.producer.send(self.topicspam,texto)
                #saveTweet('spam',tweet)
            #else:
                #print(guess + ':\n' + texto + '\n')
                #self.producer.send('drawtopic',texto)
                #saveTweet('spam',tweet)
            if self.numstop == 0:
                return False
        return True

def help(bad,good,spam,tweet):
    scoregood = 0.0
    scorebad = 0.0
    tokens = nltk.word_tokenize(tweet)
    for w in tokens:
        w= w.encode('utf-8')
        w= w.lower()
        if w in good.keys():
            scoregood += good[w]
        if w in bad.keys():
            scorebad += bad[w]
    return (scoregood,scorebad)
            


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

class Learning():
    def __init__(self,bad,good,spam,tracker,stop,user):
        self.tracker = tracker
        self.feed= TwitterFeed
        self.t = Thread2(target=self.feed , args=(bad,good,spam,self.tracker,stop,user,))
        

    def start(self):
        self.t.start()
        self.t.join()
        return True
        
    def stop(self):
        self.t.stop()
        
