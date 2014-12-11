#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import pymorphy2
import re
from collections import OrderedDict

morph = pymorphy2.MorphAnalyzer()

with codecs.open('onegin', 'r', encoding='utf-8') as input:
    input_text = input.read().lower()
    input_text = re.sub('[?,-.!/;:]', '', input_text)
    words = input_text.split()

    C = {}
    for word in words:
        word_norm = morph.parse(word)[0].normal_form    
        C[word_norm] = C[word_norm] + 1 if word_norm in C else 1

    C_sorted = OrderedDict(sorted(C.iteritems(), key=lambda x: x[1], reverse=True))


    with codecs.open('out', 'w', encoding='utf-8') as out:
        for word in C_sorted:
            out.write('%s: %d\n' % (word, C_sorted[word]))