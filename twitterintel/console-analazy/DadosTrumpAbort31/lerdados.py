import nltk
from operator import itemgetter
import collections
from collections import OrderedDict

f=open("goodword.txt")
array = {}
for line in f:
    for w in nltk.word_tokenize(line):
        if w.isdigit():
            array[aux]=int(w)
        else:
            array[w]=0
            aux=w
array = OrderedDict(sorted(array.items(), key= lambda t: t[1]))
items = array.items()
items.reverse()
array = OrderedDict(items)
f.close()
f=open("goodword2.txt","w")
for line in array:
    f.write(str(line) + ' : '+ str(array[line]) + '\n')
f.close()
