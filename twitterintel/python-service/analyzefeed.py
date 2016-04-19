from kafka import KafkaConsumer
from kafka import KafkaProducer
import thread
import tweepy
import nltk
import json
import math
import threading
import sys
import pymongo
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment 


class TwitterFeed():
    def __init__(self,bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,track,stop):
        consumer_key = "eaFmBSxUveRJfmyZYeabti9Q9"
        consumer_secret= "ADf76fi3O1lKMzBxWnjqf93l3GHv28uar3bkblkvyBrAyoA23i"
        acess_token= "702208758362087425-HZiyl1x7Bh98cQa1WLBDYylyu10Bpl7"
        acess_token_secret= "IiNOTfgE3tEZvW2HDQhRKPMoOLU43NXJCXk8maj51SdAT"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(acess_token,acess_token_secret)
        self.stream = tweepy.Stream(auth, TwitterListener(bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,stop))
        self.stream.filter(track=[track])
        
    
    def close(self):
        self.stream.disconnect()
        return True

class TwitterListener(tweepy.StreamListener):
    def __init__(self,bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,stop):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.topicbad = 'badtopic'
        self.topicgood = 'goodtopic'
        self.topicspam= 'spamtopic'
        self.bad = bad
        self.good= good
        self.spam = spam
        self.bad2 = bad2
        self.good2= good2
        self.spam2 = spam2
        self.bad3 = bad3
        self.good3= good3
        self.spam3 = spam3
        self.numstop = stop

    def on_data(self, data):
        stop=set(nltk.corpus.stopwords.words('english'))
        stop.update(['http','https','rt'])
        tweet = json.loads(data)
        texto = tweet['text'].encode('ascii','replace')
        if 'text' in tweet:
            self.numstop -=1
            tokens = nltk.word_tokenize(tweet['text'])
            guess = help(self.bad,self.good,self.spam,tweet['text'])
            #guess2= help(self.bad2,self.good2,self.spam2,texto)
            #guess3= help(self.bad3,self.good3,self.spam3,texto)
            print('RealTweet: ' + texto + '\n')
            if guess=='pos': #and (guess2=='pos' or guess3=='pos'):
                print('Positive: ' + texto + '\n')
                self.producer.send(self.topicgood,texto)
                saveTweet('pos',tweet)
            elif guess=='neg': #and (guess2=='neg' or guess3=='neg'):
                print('Negative: ' + texto + '\n')
                self.producer.send(self.topicbad,texto)
                saveTweet('neg',tweet)
            elif (guess=='spam'): #and guess2=='spam' and guess3=='spam'):
                print('Spam: ' + texto + '\n')
                self.producer.send(self.topicspam,texto)
                saveTweet('spam',tweet)
            else:
                print(guess + ':\n' + texto + '\n')
                self.producer.send('drawtopic',texto)
                saveTweet('spam',tweet)
            if self.numstop == 0:
                return False
        return True

def help(bad,good,spam,tweet):
        contagempos = 0.0
        contagemneg = 0.0
        contagemspam = 0.0

        fil = open("hj.txt","w")
        aux ='drawposneg'
        texto = ''
        stop=set(nltk.corpus.stopwords.words('english'))
        stop.update(['http','https','rt'])
        tokens = nltk.word_tokenize(tweet)
        for w in tokens:
            w = w.lower()
            w = w.encode('ascii', 'replace')
            if w.isalpha() and w not in stop:
                if w in bad.keys():
                    auxbad = bad[w]
                else:
                    auxbad = 1.0
                if w in good.keys():
                    auxgood = good[w]
                else:
                    auxgood = 1.0
                if w in spam.keys():
                    auxspam = spam[w]
                else:
                    auxspam = 1.0


                if w in good.keys():
                    contagempos= contagempos + math.log10((good[w] / (auxbad+auxspam) ) )
                if w in bad.keys():
                    contagemneg= contagemneg + math.log10((bad[w] / (auxbad+auxspam)))
                if w in spam.keys():
                    contagemspam= contagemspam + math.log10((spam[w] / (auxbad+auxspam)))

        vs = vaderSentiment(tweet.encode('ascii','replace'))
        contagemneg= contagemneg * vs['neg']
        contagempos= contagempos * vs['pos']
        contagemspam = contagemspam * vs['neu']

        if(contagemspam > contagemneg) and (contagemspam > contagempos):
            aux='spam'
        elif(contagempos > contagemneg) and (contagempos > contagemspam):
            aux='pos'
        elif(contagemneg > contagemspam) and (contagemneg > contagempos):
            aux='neg'
        elif(contagemspam == contagemneg):
            aux='drawspamneg'
        elif(contagemspam == contagempos):
            aux='drawspampos'
        else:
            aux='naosei' 
        #fil.write(texto + ' ' + str(contagemneg) + ' ' + str(contagempos) + ' ' + str(contagemspam) + '\n')
        fil.close()
        return aux


def saveTweet(tipo, tweet):
    db = pymongo.MongoClient()
    board = db.BOARD
    id_str= tweet['user']['id']
    n_followers=tweet['user']['followers_count']
    location= tweet['user']['location']
    name = tweet['user']['name']
    friends_count = tweet['user']['friends_count']
    
    if(tipo == 'pos'):
        board.goodcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.goodcounter.find_one()
        auxcount = auxcount["count"]
        board.goodinfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count})

    elif(tipo == 'neg'):
        board.badcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.badcounter.find_one()
        auxcount = auxcount["count"]
        board.badinfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count})

    elif(tipo == 'spam'):
        board.spamcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.spamcounter.find_one()
        auxcount = auxcount["count"]
        board.spaminfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count})


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
    def __init__(self,bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,tracker,stop):
        self.tracker = tracker
        self.feed= TwitterFeed
        self.t = Thread2(target=self.feed , args=(bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,self.tracker,stop,))
        

    def start(self):
        self.t.start()
        return self.t
        
    def stop(self):
        self.t.stop()
        
