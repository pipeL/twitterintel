import web
import pymongo
import tweepy
import nltk
import json
import threading
import sys
import time
from bson.objectid import ObjectId
from kafka import KafkaProducer

from instantfeed import InstantFeed as feed
from learningonline import Learning as learn

from analazyperceptron import AnalyzerPerceptron
from analazyperceptronfeed import Learning as perce

from analyzefeed import Learning as analy
from analyze import Analyzer


urls= ( '/InstantFeed','InstantFeed',
        '/GetDataInstantFeed','GetDataInstantFeed',
        '/Learning', 'Learning',
        '/getTotal','getTotal',
        '/getTweetsGood','getTweetsGood',
        '/getTweetsBad','getTweetsBad',
        '/getTweetsSpam','getTweetsSpam',
        '/getTopWordGood','getTopWordGood',
        '/getTopWordBad','getTopWordBad',
        '/getTopWordSpam','getTopWordSpam',
        '/getTopTwoWordGood','getTopTwoWordGood',
        '/getTopTwoWordBad','getTopTwoWordBad',
        '/getTopTwoWordSpam','getTopTwoWordSpam',
        '/getTopThreeWordGood','getTopThreeWordGood',
        '/getTopThreeWordBad','getTopThreeWordBad',
        '/getTopThreeWordSpam','getTopThreeWordSpam',
        '/Results', 'Results',
        '/getWordProbGood','getWordProbGood',
        '/getWordProbBad','getWordProbBad',
        '/getWordProbSpam','getWordProbSpam',
        '/StartFeed','StartFeed',
        '/Register','Register',
        '/getInfoTweetsGood','getInfoTweetsGood',
        '/getInfoTweetsBad','getInfoTweetsGood',
        '/getWordProbPerceptronGood','getWordProbPerceptronGood',
        '/getWordProbPerceptronBad','getWordProbPerceptronBad',
        '/StartFeedPerceptron','StartFeedPerceptron',
        '/Login','Login',
        '/CheckStatus','CheckStatus',
        '/StartFeedModifie','StartFeedModifie',
	'/Contact','Contact'
      )


class InstantFeed:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db = pymongo.MongoClient()
        user_data= web.input(id={})
        data = user_data.id
        data = json.loads(str(data))
        user = str(data[2])
        number = int(data[1])
        aux = 'INSTANT'+user
        db.drop_database(aux)
        self.aux = feed(str(data[0]),number,user)
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"true"}},upsert=True)
        self.aux.start()
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"false"}},upsert=True)
        send={}
        send[0]='true'
        return json.dumps(send)

class GetDataInstantFeed:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db=pymongo.MongoClient()
        user_data=web.input(id="no data")
        user = str(user_data.id)
        aux = 'INSTANT'+user
        send = {}
        data = db[aux].tweet.find()
        count = 0
        send['tweet']={}
        send['word']={}
        send['twoword']={}
        send['threeword']={}
        for line in data:
            send['tweet'][count]=line['tweet']
            count+=1
        count=0
        data = db[aux].wordcole.find()
        for line in data:
            send['word'][count]={}
            send['word'][count]['count']=line['count']
            send['word'][count]['word']=line['word']
            count+=1
        count=0
        data = db[aux].twowordcole.find()
        for line in data:
            send['twoword'][count]={}
            send['twoword'][count]['count']=line['count']
            send['twoword'][count]['word']=line['word']
            count+=1
        count=0
        data = db[aux].threewordcole.find()
        for line in data:
            send['threeword'][count]={}
            send['threeword'][count]['count']=line['count']
            send['threeword'][count]['word']=line['word']
            count+=1
        
        send = json.dumps(send)
        return send





#First class to be called
#Learning class = get a feed of 100 tweets based on topic passed as id
#After the feed is complete return the data=Tweets
#Data will be displayed in application for classification
class Learning:
    def GET(self):
        send = {}
        count = 0
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data= web.input(id={})
        data = user_data.id
        data = json.loads(str(data))
        user = str(data[2])
        number = int(data[1])
        db = pymongo.MongoClient()
        db.drop_database("LEARNING"+str(data[2]))
        db.drop_database("SPAM"+str(data[2]))
        db.drop_database("BAD"+str(data[2]))
        db.drop_database("GOOD"+str(data[2]))
        db.drop_database("BOARD"+str(data[2]))
        auxuser ='LEARNING'+str(data[2])
        aux = learn(data[0],data[1],str(data[2]))
        t = threading.Thread(target=aux.start)
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"true"}},upsert=True)
        t.start()
        t.join()
        #time.sleep(1)
        #if t.is_alive():    IMPORTANTE PARA PARAR MESMO QUE CONTINUE O THREAD
            #sys.exit()
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"false"}},upsert=True)
        
        data = db[auxuser].online.find()
        for line in data:
            send[count]=line['tweet']
            count+=1
        if count < number:
            send[0]='false'
        send = json.dumps(send)
        return send


#Second function to be called
class Results:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data= web.input(id={})
        data = user_data.id
        data = json.loads(str(data))
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        goodtopic= 'goodtopic'
        badtopic= 'badtopic'
        spamtopic ='spamtopic'
        stop=set(nltk.corpus.stopwords.words('english'))
        stop.update(['http','https','rt'])
        db=pymongo.MongoClient()


        user = str(data['0']['user'])
        aux = 'LEARNING'+user
        
        for line in data:
            texto = ''
            tokens = nltk.word_tokenize(data[line]['tweet'])
            for w in tokens:
                w = w.lower()
                w = w.encode('utf-8')
                if w.isalpha() and w not in stop:
                    texto=texto + ' ' + w
            texto = texto.encode('utf-8')
            #Save that into learning db for changes if wanted 
            if(data[line]['answer']=='Good'):
                db[aux].goodlearning.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
                texto = user + '-' + texto
                producer.send(goodtopic,texto)
            if(data[line]['answer']=='Bad'):
                db[aux].badlearning.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
                texto = user + '-' + texto
                producer.send(badtopic,texto)
            #if(data[line]['answer']=='Spam'):
                #self.producer.send(self.spamtopic,texto)
        return 'algo'



#After the classification is done Class to be called to Start Feed Analyses based on data classificated
#This class uses Two Class kept in different .py files
#Analyzer(class) getGoodDataWord(function)
#getGoodDataWord will return the 3 variables containing the probability of each word present in tweets classified(GOOD,BAD,SPAM)
#After getting the probabilities calls analy class responsable for start feed with classification based on probability of each word

#FEED AUTOMATICLY STOPS AFTER 1000 TWEETS 



#START FEED WITH DATA MODIFIE BY USER
class StartFeedModifie:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data = web.input(id=" ")
        data = user_data.id
        data = json.loads(data)
        user = str(data['5'])
        #fil = open('hj.txt','w')
        db = pymongo.MongoClient()
        db.drop_database("BOARD"+user)
        a={}
        b={}
        c={}
        print user
        for line in data['3']:
            a[line]=float(data['3'][line])
        for line in data['2']:
            b[line]=float(data['2'][line])
        for line in data['4']:
            c[line]=float(data['4'][line])
        (a2,b2,c2)=Analyzer(user).getGoodDataTwoWord()
        (a3,b3,c3)=Analyzer(user).getGoodDataThreeWord()
        number = int(data['1'])
        self.aux = analy(a,b,c,a2,b2,c2,a3,b3,c3,str(data['0']),number,user)
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"true"}},upsert=True)
        self.aux.start()
        #print(str(a) + '\n\n\n' + str(b) + '\n\n\n' + str(c))
        #raw_input()
        #print "start"
        #print a
        #time.sleep(120)
        #print "end"
        #aux.stop()
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"false"}},upsert=True)
        send={}
        auxuser = 'BOARD'+user
        countgood = db[auxuser].goodcounter.find_one()
        if countgood != None:
            countgood = int(countgood["count"])
        else:
            countgood = 0
        countbad = db[auxuser].badcounter.find_one()
        if countbad != None:
            countbad = int(countbad["count"])
        else:
            countbad=0
        print countbad
        print countgood
        print number
        if ((countbad+countgood)< number):
            send[0]='false'
        else:
            send[0]='true'
        send = json.dumps(send)
        return send


#FALTA CONFIGURAR DATABASE
class StartFeedPerceptron:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        #fil = open('hj.txt','w')
        db = pymongo.MongoClient()
        db.drop_database("BOARD")
        user_data = web.input(id=" ")
        data = user_data.id
        data = json.loads(data)
        number = data[1]
        (a,b,c)=AnalyzerPerceptron(10,data[4]).getGoodDataWord()
        self.aux = perce(a,b,c,str(data[0]),number,data[4])
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"true"}},upsert=True)
        self.aux.start()
        db.LOGIN.login.update({"_id":int(user)},{"$set": {"status":"false"}},upsert=True)
        return 'OK'


#ALL SERVICE FUNCTIONS RESPONSABLE FOR RETURN DATA TO WEBSITE TO BE USED IN GRAPHS


#FALTA CONFIGURAR DATABASE
class getWordProbPerceptronGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data=web.input(id=" ")
        user = str(user_data.id)
        send = {}
        (a,b,c)=AnalyzerPerceptron(10,user).getGoodDataWord()
        b = json.dumps(b)
        return b
class getWordProbPerceptronBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data=web.input(id=" ")
        user = str(user_data.id)
        send = {}
        (a,b,c)=AnalyzerPerceptron(10,user).getGoodDataWord()
        a = json.dumps(a)
        return a
#GET WORDS POSTERIOUR PROBABILITY
class getWordProbGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data=web.input(id=" ")
        user = str(user_data.id)
        send = {}
        (a,b,c)=Analyzer(user).getGoodDataWord()
        b = json.dumps(b)
        return b
        
class getWordProbSpam:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data=web.input(id="no data")
        user = str(user_data.id)
        send = {}
        (a,b,c)=Analyzer(user).getGoodDataWord()
        c = json.dumps(c)
        return c

class getWordProbBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data=web.input(id=" ")
        user = str(user_data.id)
        send = {}
        (a,b,c)=Analyzer(user).getGoodDataWord()
        a = json.dumps(a)
        return a
        

class getTweetsGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        user_data=web.input(id="no data")
        user = str(user_data.id)
        send = {}
        count = 0
        aux = 'BOARD'+user
        self.db=pymongo.MongoClient()
        data = self.db[aux].good.find()
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
        user_data=web.input(id="no data")
        user = str(user_data.id)
        send = {}
        count = 0
        aux = 'BOARD'+user
        self.db=pymongo.MongoClient()
        data = self.db[aux].bad.find()
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
        user_data=web.input(id="no data")
        user = str(user_data.id)
        send = {}
        count = 0
        aux = 'BOARD'+user
        self.db=pymongo.MongoClient()
        data = self.db[aux].spam.find()
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
        user_data=web.input(id="no data")
        user = str(user_data.id)
        auxuser = 'BOARD'+user
        self.db=pymongo.MongoClient()
        bom = self.db[auxuser].goodcounter.find_one()
        mau = self.db[auxuser].badcounter.find_one()
        spam = self.db[auxuser].spamcounter.find_one()
        send = {}
        send[0]={}
        send[1]={}
        #send[2]={}
        if(bom!= None):
            send[0]["contagem"] = bom['count']
        else:
            send[0]["contagem"]=0
        if(mau!=None):
            send[1]["contagem"] = mau['count']
        else:
            send[1]["contagem"]=0
        send[0]["tipo"] = 'bom'
        send[1]["tipo"] = 'mau'
        #send[2]["contagem"] = spam['count']
        #send[2]["tipo"] = 'spam'
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
        user = str(user_data.id)
        auxuser = 'GOOD'+user
        query = self.db[auxuser].wordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send


class getTopTwoWordGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        user = str(user_data.id)
        auxuser = 'GOOD'+user
        query = self.db[auxuser].twowordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send

class getTopThreeWordGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        user = str(user_data.id)
	auxuser = 'GOOD'+user
        query = self.db[auxuser].threewordcole.find().sort("count",pymongo.DESCENDING).limit(40)
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
        user = str(user_data.id)
        auxuser = 'BAD'+user
        query = self.db[auxuser].wordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send

class getTopTwoWordBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        user = user_data.id
        auxuser = 'BAD'+user
        query = self.db[auxuser].twowordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send


class getTopThreeWordBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        user = str(user_data.id)
        auxuser = 'BAD'+user
        query = self.db[auxuser].threewordcole.find().sort("count",pymongo.DESCENDING).limit(40)
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
        user = str(user_data.id)
        auxuser = 'SPAM'+user
        query = self.db[auxuser].wordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send

class getTopTwoWordSpam:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        user = str(user_data.id)
        auxuser = 'SPAM'+user
        query = self.db[user].twowordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send

class getTopThreeWordSpam:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id="no data")
        self.db=pymongo.MongoClient()
        user = str(user_data.id)
        auxuser = 'SPAM'+user

        query = self.db[auxuser].threewordcole.find().sort("count",pymongo.DESCENDING).limit(40)
        for line in query:
            send[count]={}
            send[count]['word']=line['word']
            send[count]['count']=line['count']
            count+=1
        send = json.dumps(send)
        return send

class getInfoTweetsGood:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id=" ")
        user = str(user_data.id)
        auxuser = 'BOARD'+user
        self.db=pymongo.MongoClient()
        query = self.db[auxuser].goodinfo.find()
        for line in query:
            send[count]={}
            send[count]['n_followers']=line['n_followers']
            send[count]['location']=line['location']
            send[count]['name']=line['name']
            send[count]['friends_count']=line['friends_count']
            send[count]['id_str']=line['id_str']
            send[count]['time']=line['time']
            count+=1
        send = json.dumps(send)
        print send
        return send

class getInfoTweetsBad:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        send = {}
        count = 0
        user_data=web.input(id=" ")
        user = str(user_data.id)
        useraux = 'BOARD'+user
        self.db=pymongo.MongoClient()
        query = self.db[useraux].badinfo.find()
        for line in query:
            send[count]={}
            send[count]['n_followers']=line['n_followers']
            send[count]['location']=line['location']
            send[count]['name']=line['name']
            send[count]['friends_count']=line['friends_count']
            send[count]['id_str']=line['id_str']
            send[count]['time']=line['time']
            count+=1
        print send
        send = json.dumps(send)
        return send

class Register:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db = pymongo.MongoClient()
        send = {}
	user_data= web.input(id={})
        data = user_data.id
        data = json.loads(str(data))
        dados = db.LOGIN.login.find()
        for line in dados:
            if(line['user']==data[0]):
                send[0]='UserExist'
                send = json.dumps(send)
                return send
        db.LOGIN.numusers.update({"type":'contagem'},{"$inc": {'count':1}},upsert=True)
        auxcount = db.LOGIN.numusers.find_one()['count']
        
        consumer_key = data[5]
        consumer_secret=data[6]
        access_token=data[7]
        access_token_secret= data[8]
        
        if(str(data[4])=='letmefeedforawhile'):
            db.LOGIN.login.insert_one({"_id": auxcount , "user":data[0] , "firstname": data[1] ,"secondname" : data[2] , "password": data[3] , "intel":'perce' , 'status':'false', 'consumer_key':consumer_key , 'consumer_secret':consumer_secret , 'access_token':access_token , 'access_token_secret' : access_token_secret})
            send[0]='True'
        elif(str(data[4])=='justtogo'):
            db.LOGIN.login.insert_one({"_id": auxcount , "user":data[0] , "firstname": data[1] ,"secondname" : data[2] , "password": data[3] , "intel":'naive' , 'status':'false', 'consumer_key':consumer_key , 'consumer_secret':consumer_secret , 'access_token':access_token , 'access_token_secret' : access_token_secret})
            send[0]='True'
        else:
           send[0]='False' 
        
        send = json.dumps(send)
        return send

class Login:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db = pymongo.MongoClient()
        send = {}
        user_data= web.input(id={})
        data = user_data.id
        data = json.loads(str(data))
        users = db.LOGIN.login.find()
        for line in users:
            if data[0] == line['user']:
                if data[1] == line['password']:
                    send[0]=line['_id']
                    send[1]=line['intel']
                    send[2]=line['status']
                    send = json.dumps(send)
                    return send
                else:
                    send[0]='False'
                    send[1]='RongPass'
                    send = json.dumps(send)
                    return send
        send[1]='RongUser'    
        send[0]='False'
        send = json.dumps(send)
        return send
            
        
class CheckStatus:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db = pymongo.MongoClient()
        send = {}
        user_data= web.input(id={})
        user = str(user_data.id)
        send[0]=db.LOGIN.login.find_one({'_id':int(user)})['status']
        send = json.dumps(send)
        return send

class Contact:
    def GET(self):
	web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        db = pymongo.MongoClient()
	user_data = web.input(id={})
	data = user_data.id
	data = json.loads(str(data))
	db.MESSAGE.message.insert_one({"_id": str(data[0]) , "user":data[1] , "subject":data[2], "Message":data[3]})

	send={}
	send[0]='true'
	return json.dumps(send)             

#SERVICE START
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()

