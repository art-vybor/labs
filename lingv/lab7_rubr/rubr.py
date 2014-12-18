#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import re
from math import log

def getVocabulary(D, V=None):
    res = {}
    for d in D:
        text = codecs.open('documents/' + d, encoding='utf-8').read()
        text = re.sub('[?—«»,-.£!"\\(\\)/;:+]', ' ', text)
        text = text.encode('utf-8')

        for word in text.split():
            if (V is None) or (V is not None and word in V):
                res[word] = res[word] + 1 if word in res else 1
    return res

def train(C, D, alpha = 0.001):
    V = getVocabulary(D)
    prior = {}
    condprob = {}

    for c in C:
        D_c = filter(lambda x: x.startswith(c), D)
        prior[c] = len(D_c)*1.0/len(D)
        T_c = getVocabulary(D_c)
        Sum_T_c = sum(T_c.values()) + len(T_c)*alpha

        for t in V:
            if t not in T_c:
                T_c[t] = 0

            if t not in condprob:
                condprob[t] = {}


            condprob[t][c] = (T_c[t]+alpha*1.0)/Sum_T_c

    return (V, prior, condprob)

def apply(C, V, prior, condprob, d='test'):
    W = getVocabulary([d], V)
    score = {}

    for c in C:
        #score[c] = log(prior[c], 10)
        score[c] = prior[c]
        for t in W:
            #print c, t, condprob[t][c]
            #score[c] += log(condprob[t][c], 10)
            score[c] += condprob[t][c]


    return score

C = ['politic', 'sport']
D = filter(lambda x: x.startswith('politic') or x.startswith('sport'), os.listdir('documents'))

V, prior, condprob = train(C, D)
score = apply(C, V, prior, condprob)

print score

for c in score:
    if score[c] == max(score.values()):
        print c

#test on train :)
# for c in C:
#     for d in filter(lambda x: x.startswith(c), D):

#         V, prior, condprob = train(C, D)
#         score = apply(C, V, prior, condprob, d)

#         for c in score:
#             if score[c] == max(score.values()):
#                 print c
#                 print d



