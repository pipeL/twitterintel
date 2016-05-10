import pymongo
import nltk.corpus

#Import storm BasicBolt
from petrel import storm
from petrel.emitter import BasicBolt 

class WordCountBolt(BasicBolt):
    def __init__(self):
        super(WordCountBolt, self).__init__(script=__file__)
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stop_words.update(['http', 'https', 'rt'])
    
    def initialize(self,conf,context):
        self.db = pymongo.MongoClient()
        
    #Doesnt emit
    def declareOutputFields(self):
        return[]

    #For each word emitted by WordDivider process will execute
    #Each time will increment the word in MONGODB 
    #DB = BAD Collection = wordcole
    def process(self,tup):
        aux = 'BAD'+tup.values[1]
        self.db[aux].wordcole.update(
            {'word':str(tup.values[0])},
            {"$inc": { 'count': 1}},
            upsert=True
        )

    #OLDER VERSION USED TO SET SPECIAL TICK
    #def getComponentConfiguration(self):
    #return {"topology.tick.tuple.freq.secs":300}

def run():
    WordCountBolt().run()
