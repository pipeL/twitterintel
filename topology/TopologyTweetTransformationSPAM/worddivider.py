import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
import nltk.corpus
import logging
from kafka import KafkaProducer

#Import storm BasicBolt
from petrel import storm
from petrel.emitter import BasicBolt


class WordDividerBolt(BasicBolt):
    def __init__(self):
        super(WordDividerBolt, self).__init__(script=__file__)
        self.stop = set(nltk.corpus.stopwords.words('english'))
        self.stop.update(['http' , 'https', 'rt'])
    
    #return of this Bolt is tuple['word'] = each word of tweet passed by KafkaConsumer
    def declareOutputFields(self):
        return['word','user']

    #*process* for each emit of KafkaConsumer this will be executed
    #use get_words to separate words from original tweet and emit them to counter bolt
    def process(self, tup):
        for word in self.get_words(tup.values[0]):
            word= word.encode('utf-8','replace')
            storm.emit([word,tup.values[1]])

    #yield each word present in sentence
    def get_words(self, sentence):
        for w in nltk.word_tokenize(sentence):
            w = w.lower()
            if w.isalpha() and w not in self.stop:
                yield w

def run():
    WordDividerBolt().run()
