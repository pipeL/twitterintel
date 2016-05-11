from aprendizagem import Learning
from analyzer import Analyzer
from analazy import TwitterAnalyze
import sys
import pymongo

tracker=u"donaldtrump , realdonaldtrump , nevertrump , votetrump"
doc = open('algo.txt','w')
db = pymongo.MongoClient()
db.drop_database("SPAM")
db.drop_database("BAD")
db.drop_database("GOOD")
db.drop_database("BOARD")

ola=Learning(tracker)
try:
    ola.start()
except:
    pass

(a,b,c)=Analyzer().getGoodDataWord()
(a2,b2,c2)=Analyzer().getGoodDataTwoWord()
(a3,b3,c3)=Analyzer().getGoodDataThreeWord()
doc.write(str(a) + '\n' + str(b) + '\n' + str(c))
doc.close()
#doc.write('\n'+str(a2) + '         ' + str(b2) + '          ' + str(c2))
#doc.write('\n'+str(a3) + '         ' + str(b3) + '          ' + str(c3))


db.drop_database("SPAM")
db.drop_database("BAD")
db.drop_database("GOOD")
db.drop_database("BOARD")


TwitterAnalyze(a,b,c,a2,b2,c2,a3,b3,c3,tracker)




