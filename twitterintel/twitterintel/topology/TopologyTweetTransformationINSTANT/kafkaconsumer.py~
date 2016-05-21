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
        
    #Consumer for 'badtopic' kafka topic 
    #Server localhost port 9092 -- Can have multiple clusters for same topic different port
    def initialize(self, conf, context):
        self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092',auto_offset_reset='earliest')
        self.db = pymongo.MongoClient()
	self.topic='badtopic'
        self.consumer.subscribe([self.topic])
        
    #The return of this spout tuple['sentence'] = tweet
    @classmethod
    def declareOutputFields(cls):
        return ['sentence']

    #Each tweet added to 'badtopic' will be a Tuple
    #For each tuple data is saved at MONGODB DB = BOARD collection = bad
    def nextTuple(self):
        for message in self.consumer:
            algo = message.value
            self.db.BOARD.bad.insert_one({'tweet':algo})
            storm.emit([algo])

def run():
    KafkaConsumerSpout().run()
