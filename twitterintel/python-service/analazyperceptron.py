import pymongo
import nltk

class AnalyzerPerceptron:

    def __init__(self,number,user):
       self.db = pymongo.MongoClient()
       self.iterations = number
       self.user = user

    def getGoodDataWord(self):
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()
        scoregood = 0.0
        scorebad= 0.0
        user = str(self.user)
        bad = 'BAD'+user
        good = 'GOOD'+user
        spam = 'SPAM'+user
        
        badword = self.db[bad].wordcole.find()
        goodword= self.db[good].wordcole.find()
        spamword= self.db[spam].wordcole.find()
        badtwoword = self.db[bad].twowordcole.find()
        goodtwoword= self.db[good].twowordcole.find()
        spamtwoword= self.db[spam].twowordcole.find()
        badthreeword = self.db[bad].threewordcole.find()
        goodthreeword= self.db[good].threewordcole.find()
        spamthreeword= self.db[spam].threewordcole.find()
        for line in goodword:
            goodrankingword[line['word']]= line['count']
        for line in goodtwoword:
            goodrankingword[line['word']]= line['count']
        for line in goodthreeword:
            goodrankingword[line['word']]= line['count']
        for line in badword:
            badrankingword[line['word']]=line['count']
        for line in badtwoword:
            goodrankingword[line['word']]= line['count']
        for line in badthreeword:
            goodrankingword[line['word']]= line['count']
        for line in spamword:
            spamrankingword[line['word']]=line['count']
        for line in spamtwoword:
            goodrankingword[line['word']]= line['count']
        for line in spamthreeword:
            goodrankingword[line['word']]= line['count']

        board = 'BOARD'+user

        for i in range(self.iterations):
            tweets = self.db[board].good.find()
            for line in tweets:
                tokens = nltk.word_tokenize(line['tweet'])
                for w in tokens:
                    w= w.encode('utf-8')
                    w= w.lower()
                    if w in goodrankingword.keys():
                        scoregood += goodrankingword[w]
                    if w in badrankingword.keys():
                        scorebad += badrankingword[w]
                if scoregood < scorebad:
                    for w in tokens:
                        w= w.encode('utf-8')
                        w= w.lower()
                        if w not in goodrankingword.keys():
                            goodrankingword[w]=0.0001
                        if w not in badrankingword.keys():
                            badrankingword[w]=0.0001
                        aux = ((badrankingword[w]-goodrankingword[w]) + 1.0) / 2
                        aux = min(0.004,aux)
                        if w in goodrankingword.keys():
                            goodrankingword[w]+=aux
                        if w in badrankingword.keys():
                            badrankingword[w]-=aux
            tweets = self.db[board].bad.find()
            for line in tweets:
                tokens = nltk.word_tokenize(line['tweet'])
                for w in tokens:
                    w = w.encode('utf-8')
                    w= w.lower()
                    if w in goodrankingword.keys():
                        scoregood += goodrankingword[w]
                    if w in badrankingword.keys():
                        scorebad += badrankingword[w]
                if scoregood < scorebad:
                    for w in tokens:
                        w= w.encode('utf-8')
                        w= w.lower()
                        if w not in goodrankingword.keys():
                            goodrankingword[w]=0.0001
                        if w not in badrankingword.keys():
                            badrankingword[w]=0.0001
                        aux = ((goodrankingword[w]-badrankingword[w]) + 1.0) / 2
                        aux = min(0.004,aux)
                        goodrankingword[w]-=aux
                        badrankingword[w]+=aux
    
        return (badrankingword,goodrankingword,spamrankingword)