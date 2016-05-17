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
        return['word' , 'user']
    
    #Same process as WordDivider
    #Instead of counting single words counts 2 words 
    #Only counts if the sentence as pair number of words
    def process(self, tup):
        if(len(tup.values[0])>1):
            count =0
            words = self.get_words(tup.values[0].encode('utf-8','ignore'))
            if len(words)>=2 and (len(words)%2)==0:
                for index in words:
                    if count ==0:
                        helpcount = words[index]
                        count+=1
                    else:
                        word2 = helpcount + ' ' + words[index]
                        count =0
                        storm.emit([word2,tup.values[1]])
            elif(len(words)>2):
                for index in words:
                    if words[len(words)-1] == words[index]:
                        word2 = words[len(words)-2] + ' ' + words[index]
                        storm.emit([word2,tup.values[1]])
                    if count ==0:
                        helpcount = words[index]
                        count+=1
                    else:
                        word2 = helpcount + ' ' + words[index]
                        count =0
                        storm.emit([word2,tup.values[1]])
            

    def get_words(self, sentence):
        count = 0
        aux = {}
        for w in nltk.word_tokenize(sentence):
            w = w.lower()
            if w.isalpha() and (w != 'https') and (w !='http') and (w!='rt'):
                aux[count]= w
                count+=1
        return aux
                 
def run():
    TwoWordDividerBolt().run()
