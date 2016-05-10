import time
import logging
#import mongo api
import pymongo
import json
#Import kafkaConsumer
from kafka import KafkaConsumer

#Import storm Spout
from petrel import storm
from petrel.emitter import Spout

class KafkaConsumerSpout(Spout):
    def __init__(self):
        super(KafkaConsumerSpout, self).__init__(script=__file__)
        
    #Consumer for 'spamtopic' kafka topic 
    #Server localhost port 9092 -- Can have multiple clusters for same topic different port
    def initialize(self, conf, context):
        self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092',auto_offset_reset='earliest')
        self.db = pymongo.MongoClient()
	self.topic='spamtopic'
        self.consumer.subscribe([self.topic])
        
    #The return of this spout tuple['sentence'] = tweet
    @classmethod
    def declareOutputFields(cls):
        return ['sentence','user']

    #Each tweet added to 'badtopic' will be a Tuple
    #For each tuple data is saved at MONGODB DB = BOARD collection = bad
    def nextTuple(self):
        for message in self.consumer:
            algo = message.value
            user = algo.rsplit('-',1)[0]
            aux = 'BOARD'+user
            algo = algo.rsplit('-',1)[1]
            self.db[aux].SPAM.insert_one({'tweet':algo})
            storm.emit([algo,user])

def run():
    KafkaConsumerSpout().run()
