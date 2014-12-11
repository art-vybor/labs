from collections import OrderedDict
import pprint
import codecs
import re
from math import log
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

train_size = 0.85
test_size = 0.15

#
#1307.70290319
#---------
#140819.746409
#

def prob(c, B, N):
    l = 0.5 #labmda

    return (c+l)/(N+B*l)

def getP(ngramms):
    C = {}
    for word in ngramms:
        C[word] = C[word] + 1 if word in C else 1
    
    B = len(C)
    N = len(ngramms)
    
    res = {}

    for ngramm in ngramms:
        if ngramm not in res:
            res[ngramm] = prob(C[ngramm], B, N)

    res['-0-'] = prob(0, B, N)

    return res #OrderedDict(sorted(res.iteritems(), key=lambda x: x[1], reverse=True))

def getPerplexy(ngramms, P):
    res = 0.0

    for word in ngramms:
        res += log(P[word], 2) if word in P else log(P['-0-'], 2)

    return  2 ** (-res/len(ngramms))

out1 = codecs.open('out1', 'w', encoding='utf-8')
out2 = codecs.open('out2', 'w', encoding='utf-8')

with codecs.open('hpmor', 'r', encoding='utf-8') as input:
    input_text = input.read().lower()
    input_text = re.sub('[?,-.!/;:]', '', input_text)
    train_len = int(train_size*len(input_text))
    train = input_text[:train_len]
    test = input_text[train_len:int(test_size*len(input_text))+train_len]

#1gramm
train = train.split()
test = test.split()

#train = [morph.parse(word)[0].normal_form for word in train]
#test = [morph.parse(word)[0].normal_form for word in test]

P_1gramm = getP(train)
print getPerplexy(test, P_1gramm)

print '---------'
#2gramm
train_2 = []
test_2 = []

for i in range(0, len(train)):
    if i != 0:
        train_2.append(' '.join([train[i-1], train[i]]))

for i in range(0, len(test)):
    if i != 0:
        test_2.append(' '.join([test[i-1], test[i]]))

P_2gramm = getP(train_2)
print getPerplexy(test_2, P_2gramm)