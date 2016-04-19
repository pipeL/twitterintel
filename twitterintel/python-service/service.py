import web
import pymongo
import tweepy
import nltk
import json
import threading
import sys
import time
from kafka import KafkaProducer
from learningonline import Learning as learn
from analyzefeed import Learning as analy
from analyze import Analyzer


urls= ( '/Learning', 'Learning',
        '/getTotal','getTotal',
        '/getTweetsGood','getTweetsGood',
        '/getTweetsBad','getTweetsBad',
        '/getTweetsSpam','getTweetsSpam',
        '/getTopWordGood','getTopWordGood',
        '/getTopWordBad','getTopWordBad',
        '/getTopWordSpam','getTopWordSpam',
        '/Results', 'Results',
        '/StartFeed','StartFeed'
      )

#First class to be called
#Learning class = get a feed of 100 tweets based on topic passed as id
#After the feed is complete return the data=Tweets
#Data will be displayed in application for classification
class Learning:
    def GET(self):
        send = {}
        count = 0
        user_data = web.input()
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db = pymongo.MongoClient()
        db.drop_database("LEARNING")
        db.drop_database("SPAM")
        db.drop_database("BAD")
        db.drop_database("GOOD")
        db.drop_database("BOARD")
        db = db.LEARNING
        track = str(user_data.id)
        aux = learn(track)
        t = threading.Thread(target=aux.start)
        t.start()
        #time.sleep(1)
        #if t.is_alive():    IMPORTANTE PARA PARAR MESMO QUE CONTINUE O THREAD
            #sys.exit()
        t.join()
        data = db.online.find()
        for line in data:
            send[count]=line['tweet']
            count+=1
        send = json.dumps(send)
        return send


#Second function to be called
#Gets the result of user classification
#Puts in the right topic according to user classification
#Topics will be Consumed by each Topoplogy(GOOD, BAD, SPAM)
class Results:
    def GET(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.goodtopic= 'goodtopic'
        self.badtopic= 'badtopic'
        self.spamtopic ='spamtopic'
        self.stop=set(nltk.corpus.stopwords.words('english'))
        self.stop.update(['http','https','rt'])
        fp = open('json.txt','w')
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data= web.input(id={})
        data = user_data.id
        data = json.loads(str(data))
        
        for line in data:
            texto = ''
            tokens = nltk.word_tokenize(data[line]['tweet'])
            for w in tokens:
                w = w.lower()
                w = w.encode('utf-8')
                if w.isalpha() and w not in self.stop:
                    texto=texto + ' ' + w
            texto = texto.encode('utf-8')
            if(data[line]['answer']=='Good'):
                self.producer.send(self.goodtopic,texto)
            if(data[line]['answer']=='Bad'):
                self.producer.send(self.badtopic,texto)
            if(data[line]['answer']=='Spam'):
                self.producer.send(self.spamtopic,texto)
        print algo


#After the classification is done Class to be called to Start Feed Analyses based on data classificated
#This class uses Two Class kept in different .py files
#Analyzer(class) getGoodDataWord(function)
#getGoodDataWord will return the 3 variables containing the probability of each word present in tweets classified(GOOD,BAD,SPAM)
#After getting the probabilities calls analy class responsable for start feed with classification based on probability of each word

#FEED AUTOMATICLY STOPS AFTER 1000 TWEETS 
class StartFeed:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        fil = open('hj.txt','w')
        user_data = web.input(id=" ")
        tracker = user_data.id
        (a,b,c)=Analyzer().getGoodDataWord()
        (a2,b2,c2)=Analyzer().getGoodDataTwoWord()
        (a3,b3,c3)=Analyzer().getGoodDataThreeWord()
        self.aux = analy(a,b,c,a2,b2,c2,a3,b3,c3,str(tracker),1000)
        self.aux.start()
        fil.write(str(a) + '\n\n\n' + str(b) + '\n\n\n' + str(c))
        #print "start"
        #print a
        #time.sleep(120)
        #print "end"
        #aux.stop()
        return 'OK'



#ALL SERVICE FUNCTIONS RESPONSABLE FOR RETURN DATA TO WEBSITE TO BE USED IN GRAPHS

class getTweetsGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        self.db=pymongo.MongoClient()
        data = self.db.BOARD.good.find()
        for line in data:
            send[count]={}
            send[count]['tweet']=line['tweet']
            count+=1
        send = json.dumps(send)
        return send

class getTweetsBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        self.db=pymongo.MongoClient()
        data = self.db.BOARD.bad.find()
        for line in data:
            send[count]={}
            send[count]['tweet']=line['tweet']
            count+=1
        send = json.dumps(send)
        return send

class getTweetsSpam:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        self.db=pymongo.MongoClient()
        data = self.db.BOARD.spam.find()
        for line in data:
            send[count]={}
            send[count]['tweet']=line['tweet']
            count+=1
        send = json.dumps(send)
        return send


class getTotal:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        self.db=pymongo.MongoClient()
        bom = self.db.BOARD.goodcounter.find_one()
        mau = self.db.BOARD.badcounter.find_one()
        spam = self.db.BOARD.spamcounter.find_one()
        send[0]={}
        send[1]={}
        send[2]={}
        send[0]["contagem"] = bom['count']
        send[0]["tipo"] = 'bom'
        send[1]["contagem"] = mau['count']
        send[1]["tipo"] = 'mau'
        send[2]["contagem"] = spam['count']
        send[2]["tipo"] = 'spam'
        send = json.dumps(send)
        return send

class getTopWordGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        number = int(user_data.id)
        query = self.db.GOOD.wordcole.find().sort("count",pymongo.DESCENDING).limit(number)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send

class getTopWordBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        number = int(user_data.id)
        query = self.db.BAD.wordcole.find().sort("count",pymongo.DESCENDING).limit(number)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send
            
class getTopWordSpam:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        number = int(user_data.id)
        query = self.db.SPAM.wordcole.find().sort("count",pymongo.DESCENDING).limit(number)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send
        
        
            

#SERVICE START
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()

