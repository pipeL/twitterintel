from collections import OrderedDict
import nltk
from operator import itemgetter
import collections
from collections import OrderedDict

f=open('goodword.txt')
array= dict()
count = 0.0
for line in f:
    for w in nltk.word_tokenize(line):
        if w.isdigit():
            array[aux]=int(w)
            count = count+int(w)
        else:
            array[w]=0
            aux=w
for i in array:
    array[i]=array[i]/count
f.close()
h = open('goodwordperc.txt','w')
h.write(str(array))
h.close()
