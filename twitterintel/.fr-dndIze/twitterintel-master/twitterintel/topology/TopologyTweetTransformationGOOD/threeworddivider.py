import nltk.corpus
import logging
from kafka import KafkaProducer


from petrel import storm
from petrel.emitter import BasicBolt

class ThreeWordDividerBolt(BasicBolt):
    def __init__(self):
        super(ThreeWordDividerBolt, self).__init__(script=__file__)
        self.stop = set(nltk.corpus.stopwords.words('english'))
        self.stop.update(['http' , 'https', 'rt'])

    def declareOutputFields(self):
        return['word','user']

    #Some process as WordDivider
    #Instead of one word it divides in 3 words
    #Only if the sentence as impar number of words
    def process(self, tup):
        count =0
        if len(tup.values[0])>2 and (len(tup.values[0])%2)!=0:
            for word in self.get_words(tup.values[0]):
                if count ==0:
                    helpcount = word
                    count+=1
		elif count ==1:
		    helpcount2 = word
                    count+=1
                else:
                    word2 = word.encode('utf-8') + ' ' + helpcount.encode('utf-8') + ' ' + helpcount2.encode('utf-8')
                    count =0
                    storm.emit([word2,tup.values[1]])
        else:
            for word in self.get_words(tup.values[0]):
                if count ==0:
                    helpcount = word
                    count+=1
		elif count ==1:
		    helpcount2 = word
                    count+=1
                else:
                    word2 = word.encode('utf-8') + ' ' + helpcount.encode('utf-8') + ' ' + helpcount2.encode('utf-8')
                    count =0
                    storm.emit([word2,tup.values[1]])

    def get_words(self, sentence):
        for w in nltk.word_tokenize(sentence):
            w = w.lower()
            if w.isalpha() and w not in self.stop:
                yield w
                 
def run():
    ThreeWordDividerBolt().run()
