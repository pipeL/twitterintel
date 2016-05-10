import pymongo
import nltk.corpus


from petrel import storm
from petrel.emitter import BasicBolt 

class TwoWordCountBolt(BasicBolt):
    def __init__(self):
        super(TwoWordCountBolt, self).__init__(script=__file__)
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stop_words.update(['http', 'https', 'rt'])
    
    def initialize(self,conf,context):
        self.db = pymongo.MongoClient()
        
    def declareOutputFields(self):
        return[]

    def process(self,tup):
        #if tup.is_tick_tuple():
            #self.emitCurrentWindowCounts()
        #else:
        aux = 'SPAM'+tup.values[1]
        self.db[aux].wordcole.update(
            {'word':str(tup.values[0])},
            {"$inc": { 'count': 1}},
            upsert=True
        )


    def getComponentConfiguration(self):
        return {"topology.tick.tuple.freq.secs":300}

def run():
    TwoWordCountBolt().run()
