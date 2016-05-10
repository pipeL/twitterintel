import logging
from collections import defaultdict
from kafka import KafkaProducer

from petrel import storm
from petrel.emitter import BasicBolt

log = logging.getLogger('kafkaproducercount')

class SlotBasedCounter(object):
    def __init__(self, numSlots):
        self.numSlots= numSlots
        self.objToCounts = defaultdict(lambda: [0] * numSlots)
        
    def incrementCount(self, obj, slot):
        self.objToCounts[obj][slot] +=1

    def getCount(self,obj , slot):
        return sel.objToCounts[obj][slot]
    
    def getCounts(self):
        return dict((k, sum(v)) for k, v in self.objToCounts.iteritems())

    def wipeSlot(self, slot):
        for obj in self.objToCounts.iterkeys():
            self.objToCounts[obj][slot] = 0
    
    def shouldBeRemovedFromCounter(self, obj):
        return sum(self.objToCounts[obj])==0

    def wipeZeros(self):
        objToBeRemoved = set()
        for obj in self.objToCounts.iterkeys():
            if sum(self.objToCounts[obj]) == 0:
                objToBeRemoved.add(obj)
        for obj in objToBeRemoved:
            del self.objToCounts[obj]

class SlidingWindowCounter(object):
    def __init__(self, windowLengthInSlots):
        self.windowLengthInSlots = windowLengthInSlots
        self.objCounter = SlotBasedCounter(self.windowLengthInSlots)
        self.headSlot = 0
        self.tailSlot = self.slotAfter(self.headSlot)

    def incrementCount(self, obj):
        self.objCounter.incrementCount(obj, self.headSlot)

    def getCountsThenAdvanceWindow(self):
        counts = self.objCounter.getCounts()
        self.objCounter.wipeZeros()
        self.objCounter.wipeSlot(self.tailSlot)
        self.headSlot=self.tailSlot
        self.tailSlot = self.slotAfter(self.tailSlot)
        return counts

    def slotAfter(self, slot):
        return (slot + 1) % self.windowLengthInSlots

class KafkaProducerCountBolt(BasicBolt):
    numWindowChunks = 5
    emitFrequencyInSeconds = 10
    windowLengthInSeconds = numWindowChunks * emitFrequencyInSeconds

    def __init__(self):
        super(KafkaProducerCountBolt, self).__init__(script=__file__)
        self.counter = SlidingWindowCounter(5)
        

    def initialize(self, conf, context):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.topic = 'spamwordcounttopic'
        
    @classmethod
    def declareOutputFields(cls):
        return ['word', 'count']
            
    def process(self, tup):       
        if tup.is_tick_tuple():
            self.emitCurrentWindowCounts()
        else:
            self.counter.incrementCount(tup.values[0])

    def emitCurrentWindowCounts(self):
        counts = self.counter.getCountsThenAdvanceWindow()
        for k, v in counts.iteritems():
            word2 = k.encode('utf-8')+ ' '+ str(v)
            self.producer.send(self.topic,word2)
            storm.emit([k, v])

    def getComponentConfiguration(self):
        return {"topology.tick.tuple.freq.secs":300}

def run():
    KafkaProducerCountBolt().run()
        
