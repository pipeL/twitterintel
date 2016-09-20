import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
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
        aux = 'INSTANT'+tup.values[1]
        self.db[aux].twowordcole.update(
            {'word':tup.values[0].encode('utf-8','ignore')},
            {"$inc": { 'count': 1}},
            upsert=True
        )

def run():
    TwoWordCountBolt().run()
