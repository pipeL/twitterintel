from kafka import KafkaConsumer
from kafka import KafkaProducer
import thread
import tweepy
import nltk
import json
import math
import time
import threading
import sys
import pymongo
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment 


class TwitterFeed():
    def __init__(self,bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,track,stop,user):
        db = pymongo.MongoClient()
        data = db.LOGIN.login.find_one({'_id':int(user)})
        consumer_key = data['consumer_key']
        consumer_secret= data['consumer_secret']
        access_token= data['access_token']
        access_token_secret= data['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        self.stream = tweepy.Stream(auth, TwitterListener(bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,stop,user),timeout=30)
        self.stream.filter(track=[track])
        
    
    def close(self):
        self.stream.disconnect()
        return True

class TwitterListener(tweepy.StreamListener):
    def __init__(self,bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,stop,user):
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
        self.user = user

    def on_data(self, data):
        fil = open("meu.txt","a")
        stop=set(nltk.corpus.stopwords.words('english'))
        stop.update(['http','https','rt'])
        tweet = json.loads(data)
        if 'text' in tweet:
            texto = tweet['text'].encode('ascii','ignore')
            self.numstop -=1
            tokens = nltk.word_tokenize(tweet['text'])
            guess = help(self.bad,self.good,self.spam,tweet['text'])
            guess2= help(self.bad2,self.good2,self.spam2,tweet['text'])
            guess3= help(self.bad3,self.good3,self.spam3,texto)
            totalguess = guess + guess2 + guess3
            #print('RealTweet: ' + texto + '\n')
            if totalguess>0: #and (guess2=='pos' or guess3=='pos'):
                #print('Positive: ' + texto + '\n')
                texto = self.user+'-'+texto
                self.producer.send(self.topicgood,texto)
                saveTweet('pos',tweet,self.user)
                saveLocation('pos',tweet,self.user)
                fil.write('POSITIVE:\n' + 'One Word:' + str(guess) + '\nTwo Word:' + str(guess2) + '\nThree Word:' + str(guess3) + '\nTotal guess:' +  str(totalguess) + '\n' + str(texto) + '\n\n\n')
                fil.close()
            elif totalguess<=0: #and (guess2=='neg' or guess3=='neg'):
                #print('Negative: ' + texto + '\n')
                texto = self.user+'-'+texto
                self.producer.send(self.topicbad,texto)
                saveTweet('neg',tweet,self.user)
                saveLocation('neg',tweet,self.user)
                fil.write('NEGATIVE:\n' + 'One Word: ' + str(guess) + '\nTwo Word:' + str(guess2) + '\nThree Word:' + str(guess3) + '\nTotal guess:' + str(totalguess) + '\n' + str(texto) + '\n\n\n')
                fil.close()

            vs = vaderSentiment(str(texto))
            contagemneg= vs['neg']
            contagempos= vs['pos']
            contagemspam=vs['neu']
            filo= open("vader.txt",'a')
            filo.write('Neg:' + str(contagemneg) + '\nPos:' + str(contagempos) + '\nNeutro:' + str(contagemspam) + '\nTotal guess:' + str(totalguess) + ' ' + str(texto) + '\n\n\n')
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
        contagempos = 0.0
        contagemneg = 0.0
        contagemspam = 0.0
        contagem = 0.0
        #numgood = float(db.LEARNING.goodlearning.find_one()['count'])
        #numbad = float(db.LEARNING.badlearning.find_one()['count'])
        #utilgood = float(numgood)
        #utilbad = float(numbad)
        #total = numbad + numgood
        #totalbad = numbad / total
        #totalgood = numgood / total
        
        texto = tweet.encode('ascii','ignore')
        stop=set(nltk.corpus.stopwords.words('english'))
        stop.update(['http','https','rt'])
        tokens = nltk.word_tokenize(tweet)
        
        for w in tokens:
            w = w.lower()
            w = w.encode('ascii', 'ignore')
            if w.isalpha() and w not in stop:
                if w in bad.keys():
                    contagemneg +=math.log10(bad[w])
                if w in good.keys():
                    contagempos +=math.log10(good[w])
            #contagemneg += math.log10(totalbad)
            #contagempos +=math.log10(totalgood)
        #print contagempos
        #print contagemneg
        if contagempos < contagemneg:
            if contagempos >= 0:
                return contagempos
            else:
                return (contagempos * -1)
        else:
            if contagemneg >= 0:
                return (contagemneg * -1)
            else:
                return contagemneg
                #if w in spam.keys():
                    #auxspam = spam[w]
                #else:
                    #auxspam = 0.000001

                #if w in good.keys():
                    #contagempos= contagempos + math.log10((good[w] / (auxbad+auxspam) ) )
                #if w in bad.keys():
                    #contagemneg= contagemneg + math.log10((bad[w] / (auxgood+auxspam)))
                #if w in spam.keys():
                    #contagemspam= contagemspam + math.log10((spam[w] / (auxbad+auxgood)))

        #vs = vaderSentiment(tweet.encode('ascii','replace'))
        #contagemneg= contagemneg * vs['neg']
        #contagempos= contagempos * vs['pos']
        #contagemspam =contagemspam * vs['neu']

        #if(contagemspam > contagemneg) and (contagemspam > contagempos):
            #aux='spam'
        #elif(contagempos > contagemneg) and (contagempos > contagemspam):
            #aux='pos'
        #elif(contagemneg > contagemspam) and (contagemneg > contagempos):
            #aux='neg'
        #elif(contagemspam == contagemneg):
            #aux='drawspamneg'
        #elif(contagemspam == contagempos):
            #aux='drawspampos'
        #else:
            #aux='naosei' 
        #fil.write(aux + ' ' + str(contagemneg) + ' ' + str(contagempos) + ' ' + str(contagemspam) + '\n')


def saveLocation(tipo,tweet,user):
    db = pymongo.MongoClient()
    board = db.BOARD
    if tweet['coordinates']:
        if tipo == 'pos':
            board.goodlocation.insert_one({"tweet":tweet['text'] , "created_at":tweet['created_at'] , "location": tweet['coordinates']})
        else:
            board.badlocation.insert_one({"tweet":tweet['text'] , "created_at":tweet['created_at'] , "location": tweet['coordinates']})
    
def saveTweet(tipo, tweet,user):
    db = pymongo.MongoClient()
    aux = 'BOARD'+user
    board = db[aux]
    id_str= tweet['user']['id']
    n_followers=tweet['user']['followers_count']
    location= tweet['user']['location']
    name = tweet['user']['name']
    friends_count = tweet['user']['friends_count']
    timenow = time.strftime("%Y-%m-%dT%H:%M:%S")

    if(tipo == 'pos'):
        board.goodcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.goodcounter.find_one()
        auxcount = auxcount["count"]
        board.goodinfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count, "time":timenow})

    elif(tipo == 'neg'):
        board.badcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.badcounter.find_one()
        auxcount = auxcount["count"]
        board.badinfo.insert_one({"_id": auxcount , "id_str":id_str , "n_followers":n_followers , "location": location , "name": name , "friends_count": friends_count, "time":timenow})

    elif(tipo == 'spam'):
        board.spamcounter.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = board.spamcounter.find_one()
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
    def __init__(self,bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,tracker,stop,user):
        self.tracker = tracker
        self.feed= TwitterFeed
        self.t = Thread2(target=self.feed , args=(bad,good,spam,bad2,good2,spam2,bad3,good3,spam3,self.tracker,stop,user,))
        

    def start(self):
        self.t.start()
        #print 'start'
        self.t.join()
        #print 'end'
        return True
        
    def stop(self):
        self.t.stop()
        
