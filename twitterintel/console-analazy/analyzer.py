import pymongo

class Analyzer:

    def __init__(self):
       self.db = pymongo.MongoClient()

       self.spam= self.db.SPAM
       self.good= self.db.GOOD
       self.bad= self.db.BAD

    def getGoodDataWord(self):
        aux={}
        max=0.0
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()
        
        badword = self.bad.wordcole.find()
        goodword= self.good.wordcole.find()
        spamword= self.spam.wordcole.find()
        for line in goodword:
            max += line['count']
        for line in badword:
            max += line['count']
        for line in spamword:
            max += line['count']
        
        badword = self.bad.wordcole.find()
        goodword= self.good.wordcole.find()
        spamword= self.spam.wordcole.find()
        for line in goodword:
            goodrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        for line in badword:
            badrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        for line in spamword:
            spamrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        return (badrankingword,goodrankingword,spamrankingword)

    def getGoodDataTwoWord(self):
        aux={}
        max=0.0
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()

        badword = self.bad.twowordcole.find()
        goodword= self.good.twowordcole.find()
        spamword= self.spam.twowordcole.find()
        for line in goodword:
            max += line['count']
        for line in badword:
            max += line['count']
        for line in spamword:
            max += line['count']
    
        badword = self.bad.wordcole.find()
        goodword= self.good.wordcole.find()
        spamword= self.spam.wordcole.find()
        for line in goodword:
            goodrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        for line in badword:
            badrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        for line in spamword:
            spamrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        return (badrankingword,goodrankingword,spamrankingword)

    def getGoodDataThreeWord(self):
        aux={}
        max=0.0
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()

        badword = self.bad.threewordcole.find()
        goodword= self.good.threewordcole.find()
        spamword= self.spam.threewordcole.find()
        for line in goodword:
            max += line['count']
        for line in badword:
            max += line['count']
        for line in spamword:
            max += line['count']
    
        badword = self.bad.wordcole.find()
        goodword= self.good.wordcole.find()
        spamword= self.spam.wordcole.find()
        for line in goodword:
            goodrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        for line in badword:
            badrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        for line in spamword:
            spamrankingword[line['word']]=(line['count']+0.01)/(max+0.01)
        return (badrankingword,goodrankingword,spamrankingword)
                    
            