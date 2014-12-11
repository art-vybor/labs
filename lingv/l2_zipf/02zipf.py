#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import re
from codecs import open
import collections
import matplotlib.pyplot as plt


split_pattern = '[ .,?!:\r\n-]'
words = {}
 
with open('book1.txt', 'r',  encoding='cp1251') as input:      
    for line in input:
        for word in filter(lambda x: len(x) > 0, re.split(split_pattern, line.replace(u'–', ' '))):
            word = word.lower()
            words[word] = 1 if word not in words else words[word] + 1
    

words = collections.OrderedDict(sorted(words.items(), key=lambda x:x[1], reverse=True))

i = 0
x = []
y = []
r = 1
print 'word\t\tf\t\tr\t\tk'
from random import randint

for word in words:
    #if randint(0, 100) < 1:
    print '%s\t\t%d\t\t%d\t\t%d' % (word, words[word], r, r*words[word])
    x.append(i)
    y.append(words[word])
    r+=1
    i+=1
    if i > 40: break

plt.plot(x,y)
fig = plt.gcf()
#plt.show()
plt.draw()
fig.savefig('1.png', dpi=100)

