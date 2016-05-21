from kafka import KafkaConsumer
from kafka import KafkaProducer
import thread
import tweepy
import nltk
import json


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
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.goodtopic= 'goodtopic'
        self.badtopic= 'badtopic'
        self.spamtopic ='spamtopic'

    def on_data(self, data):
        tweet = json.loads(data)
        texto = ''
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nTWEETS:\n')
        print('Good(g) Bad(b) SPAM(s):\n')
        if 'text' in tweet:
            tokens = nltk.word_tokenize(tweet['text'])
            for w in tokens:
                w = w.lower()
                w = w.encode('utf-8')
                if w.isalpha() and w not in self.stop:
                    texto=texto + ' ' + w
            texto = texto.encode('utf-8')
            print(tweet['text']+'\n')
            choice = raw_input('choice:')
            if choice == 'g':
                self.producer.send(self.goodtopic,texto)
            elif choice == 'b':
                self.producer.send(self.badtopic,texto)
            elif choice == 's':
                self.producer.send(self.spamtopic,texto)
            elif choice == 'q':
                return False
        return True

class Learning():
    def __init__(self,tracker):
        self.tracker = tracker
        self.feed= TwitterFeed
        #self.start()
        

    def start(self):
        thread.start_new_thread(self.feed(self.tracker),('Thread-1',1))
        
    def stop(self):
        self.feed.close()
        
