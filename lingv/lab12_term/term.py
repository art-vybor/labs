#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re
import pymorphy2
import collections
import math

morph = pymorphy2.MorphAnalyzer()

text = codecs.open('law', encoding='utf-8').read()
text = re.sub('[?—«»,-.£!"\\(\\)/;:+]', ' ', text)
text = text


collection = {}
words = {}
adj = ''

for word in text.split():
    if len(word) > 2:
        m_word = morph.parse(word)[0]
        word = m_word.normal_form
        pos = m_word.tag.POS

        words[word] = words[word] + 1 if word in words else 1

        if pos == 'ADJF':
            adj = word
        elif pos == 'NOUN' and adj != '':
            k = (adj, word)

            if k in collection:
                collection[k] +=1
            else:
                collection[k] = 1
        else:
            adj = ''


collection =  collections.OrderedDict(sorted(collection.items(), key=lambda x:x[1], reverse=True))

i = 0
for k, v in collection.iteritems():
    print ' '.join(k).encode('utf-8'), v
    i+=1
    if i == 10: break

MI = {}

for word1 in words:
    for word2 in words:
        if (word1, word2) in collection:
            M = collection[(word1, word2)] * len(words)*1.0 / (words[word1] * words[word2])
            MI[(word1, word2)] = math.log(M,2)
 
print '----------------'  
MI =  collections.OrderedDict(sorted(MI.items(), key=lambda x:x[1], reverse=True))

i = 0
for k, v in MI.iteritems():
    print ' '.join(k).encode('utf-8'), v
    i+=1
    if i == 10: break