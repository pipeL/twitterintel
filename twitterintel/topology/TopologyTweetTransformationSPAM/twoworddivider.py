import nltk.corpus
import logging
from kafka import KafkaProducer


from petrel import storm
from petrel.emitter import BasicBolt


log = logging.getLogger('twoword')

log.debug('randomsentence loading')

class TwoWordDividerBolt(BasicBolt):
    def __init__(self):
        super(TwoWordDividerBolt, self).__init__(script=__file__)
        self.stop = set(nltk.corpus.stopwords.words('english'))
        self.stop.update(['http' , 'https', 'rt'])

    def declareOutputFields(self):
        return['word']
    
    #Same process as WordDivider
    #Instead of counting single words counts 2 words 
    #Only counts if the sentence as pair number of words
    def process(self, tup):
        count =0
        if len(tup.values[0])>1 and (len(tup.values[0])%2)==0:
            for word in self.get_words(tup.values[0]):
                if count ==0:
                    helpcount = word
                    count+=1
                else:
                    word2 = word.encode('utf-8') + ' ' + helpcount.encode('utf-8')
                    count =0
                    storm.emit([word2])

    def get_words(self, sentence):
        for w in nltk.word_tokenize(sentence):
            w = w.lower()
            if w.isalpha() and w not in self.stop:
                yield w
                 
def run():
    TwoWordDividerBolt().run()
