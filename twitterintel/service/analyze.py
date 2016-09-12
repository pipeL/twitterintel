import pymongo

class Analyzer:

    def __init__(self,user):
       
       self.user=user

    def getGoodDataWord(self):
        db = pymongo.MongoClient()
        aux={}
        max=0.0
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()
        auxuser = 'LEARNING'+self.user
        auxspam = 'SPAM'+self.user
        auxgood = 'GOOD'+self.user
        auxbad = 'BAD'+self.user

        badword = db[auxbad].wordcole.find()
        goodword= db[auxgood].wordcole.find()
        spamword= db[auxspam].wordcole.find()
        countgood = float(db[auxuser].goodlearning.find_one()['count'])
        countbad = float(db[auxuser].badlearning.find_one()['count'])
        #countspam = float(db[auxuser].spamlearning.find_one()['count'])
        for line in goodword:
            max += 1
        for line in badword:
            max += 1
        for line in spamword:
            max += 1
        
        badword = db[auxbad].wordcole.find()
        goodword= db[auxgood].wordcole.find()
        spamword= db[auxspam].wordcole.find()
        for line in goodword:
            goodrankingword[line['word']]=(line['count']+0.01)/((countgood+0.01) * max)
        for line in badword:
            badrankingword[line['word']]=(line['count']+0.01)/((countbad+0.01) * max)
        for line in spamword:
            spamrankingword[line['word']]=(line['count']+0.01)/((countspam+0.01) *max)
        return (badrankingword,goodrankingword,spamrankingword)

    def getGoodDataTwoWord(self):
        db = pymongo.MongoClient()
        aux={}
        max=0.0
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()
        auxspam = 'SPAM'+self.user
        auxgood = 'GOOD'+self.user
        auxbad = 'BAD'+self.user
        badword = db[auxbad].wordcole.find()
        goodword= db[auxgood].wordcole.find()
        spamword= db[auxspam].wordcole.find()
        auxuser = 'LEARNING'+self.user
        countgood = float(db[auxuser].goodlearning.find_one()['count'])
        countbad =  float(db[auxuser].badlearning.find_one()['count'])
        #countspam = float(db[auxuser].spamlearning.find_one()['count'])
        for line in goodword:
            max += 1
        for line in badword:
            max += 1
        for line in spamword:
            max += 1
        auxspam = 'SPAM'+self.user
        auxgood = 'GOOD'+self.user
        auxbad = 'BAD'+self.user
        badword = db[auxbad].wordcole.find()
        goodword= db[auxgood].wordcole.find()
        spamword= db[auxspam].wordcole.find()
        for line in goodword:
            goodrankingword[line['word']]=(line['count']+0.01)/((countgood+0.01) * max)
        for line in badword:
            badrankingword[line['word']]=(line['count']+0.01)/((countbad+0.01) * max)
        for line in spamword:
            spamrankingword[line['word']]=(line['count']+0.01)/((countspam+0.01) *max)
        return (badrankingword,goodrankingword,spamrankingword)

    def getGoodDataThreeWord(self):
        db = pymongo.MongoClient()
        aux={}
        max=0.0
        badrankingword= dict()
        goodrankingword=dict()
        spamrankingword=dict()
        auxspam = 'SPAM'+self.user
        auxgood = 'GOOD'+self.user
        auxbad = 'BAD'+self.user
        auxuser = 'LEARNING'+self.user
        badword = db[auxbad].wordcole.find()
        goodword= db[auxgood].wordcole.find()
        spamword= db[auxspam].wordcole.find()
        countgood = float(db[auxuser].goodlearning.find_one()['count'])
        countbad = float(db[auxuser].badlearning.find_one()['count'])
        #countspam = float(db[auxuser].spamlearning.find_one()['count'])
        for line in goodword:
            max += 1
        for line in badword:
            max += 1
        for line in spamword:
            max += 1
    
        badword = db[auxbad].wordcole.find()
        goodword= db[auxgood].wordcole.find()
        spamword= db[auxspam].wordcole.find()
        for line in goodword:
            goodrankingword[line['word']]=(line['count']+0.01)/((countgood+0.01) * max)
        for line in badword:
            badrankingword[line['word']]=(line['count']+0.01)/((countbad+0.01) * max)
        for line in spamword:
            spamrankingword[line['word']]=(line['count']+0.01)/((countspam+0.01) *max)
        return (badrankingword,goodrankingword,spamrankingword)
                    
            
