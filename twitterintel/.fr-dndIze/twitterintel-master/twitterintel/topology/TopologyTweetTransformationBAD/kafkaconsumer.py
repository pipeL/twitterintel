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
        return ['sentence','user']

    #Each tweet added to 'badtopic' will be a Tuple
    #For each tuple data is saved at MONGODB DB = BOARD collection = bad
    def nextTuple(self):
        #file = open('/home/pipe/twitterintel/topology/texto.txt','a')
        for message in self.consumer:
            #file.write(str(message.value))
            algo = message.value
	    if(len(algo) >4):
            	user = algo[:1]
            	if user.isdigit():
                	aux = 'BOARD'+user
                	algo = algo[2:len(algo)]
                	if(algo[0] == ' '):
                    		algo=algo[1:len(algo)]
                	self.db[aux].bad.insert_one({'tweet':algo})
                	storm.emit([algo,user])

def run():
    KafkaConsumerSpout().run()
