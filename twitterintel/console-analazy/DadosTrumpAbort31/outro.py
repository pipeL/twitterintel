#from collections import OrderedDict
#d = {}
#f = open('goodwordperc.txt')
#for line in f:
#    tmp = line.strip().split(':')
#    d[tmp[0]]=tmp[1]
#    print(tmp[0])


import csv
studentReader = csv.reader(open('goodword.txt', 'rb'), delimiter=':', skipinitialspace=True)
d = dict()
for row in studentReader:
    d[row[0]] = tuple(row[1])
    print(row)
