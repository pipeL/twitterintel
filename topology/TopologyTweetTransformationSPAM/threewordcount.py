import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
import pymongo
import nltk.corpus


from petrel import storm
from petrel.emitter import BasicBolt 

class ThreeWordCountBolt(BasicBolt):
    def __init__(self):
        super(ThreeWordCountBolt, self).__init__(script=__file__)
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
	if(len(tup.values[1]==1)):
	        aux='SPAM'+tup.values[1]
        self.db[aux].threewordcole.update(
            {'word':tup.values[0].encode('utf-8','ignore')},
            {"$inc": { 'count': 1}},
            upsert=True
        )


    def getComponentConfiguration(self):
        return {"topology.tick.tuple.freq.secs":300}

def run():
    ThreeWordCountBolt().run()
