from collections import OrderedDict
import pprint
import codecs
import re
from math import log

train_size = 0.10
test_size = 0.15

def Prob(c, B, N):
    l = 0.5 #labmda

    return (c+l)/(N+B*l)

def getP(ngramms, _B=False):
    N = len(ngramms)
    C = {}
    for word in ngramms:
        C[word] = C[word] + 1 if word in C else 1
    
    B = len(set(' '.join(C.keys()).split()))

    if _B:
        B = B*B
    
    res = {}

    for ngramm in ngramms:
        res[ngramm] = Prob(C[ngramm], B, N)

    return OrderedDict(sorted(res.iteritems(), key=lambda x: x[1], reverse=True))

def getPerplexy(ngramms, P):
    res = 0.0

    C = {}
    for word in ngramms:
        C[word] = C[word] + 1 if word in C else 1

    #length = 0
    for word in C:    
        if word in P:
            res += C[word] * log(P[word], 2)
            #length += C[word]
    
    return  2 ** (-res/len(ngramms))



out1 = codecs.open('out1', 'w', encoding='utf-8')
out2 = codecs.open('out2', 'w', encoding='utf-8')

with codecs.open('hpmor', 'r', encoding='utf-8') as input:
    input_text = input.read().lower()
    input_text = re.sub('[?,-.!/;:]', '', input_text)
    train_len = int(train_size*len(input_text))
    train = input_text[:train_len]
    test = input_text[train_len:int(test_size*len(input_text))+train_len]


train = train.split()
test = test.split()

#1gramm
P_1gramm = getP(train)

#for ngramm in P_1gramm:
#    out1.write('%s: %f\n' % (ngramm, P_1gramm[ngramm]))


print getPerplexy(test, P_1gramm)


#2gramm
train_2 = []
test_2 = []

for i in range(0, len(train)):
    if i != 0:
        train_2.append(' '.join([train[i-1], train[i]]))

P_2gramm = getP(train_2, True)

for i in range(0, len(test)):
    if i != 0:
        test_2.append(' '.join([test[i-1], test[i]]))

print getPerplexy(test_2, P_2gramm)
#for ngramm in P_2gramm:
#    out2.write('%s: %f\n' % (ngramm, P_2gramm[ngramm]))


