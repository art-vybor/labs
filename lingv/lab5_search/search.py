#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymorphy2
import re
import codecs
import math
import collections
import sys

morph = pymorphy2.MorphAnalyzer()

def get_doc_vector(doc, inverse_index, len_docs):
    doc_vector = {}

    C = {}
    for word in doc:
        C[word] = C[word] + 1 if word in C else 1

    for word in doc:
        if word not in doc_vector:
            tf = C[word] * 1.0 / len(doc)    
            idf = math.log(len_docs+1.000001 / len(inverse_index[word]), 10)
            doc_vector[word] = tf * idf

    norm_coef = math.sqrt(sum([x**2 for x in doc_vector.values()]))

    for word in doc_vector:
        doc_vector[word] /= norm_coef

    return doc_vector

def get_doc(doc_path):
    doc = codecs.open(doc_path, 'r', encoding='utf-8').read().lower()
    doc = re.sub(ur'[?—,-.!\(\)/;:]', '', doc, re.UNICODE) #TODO braces
    return [morph.parse(word)[0].normal_form for word in doc.split()]

def get_inverse_index(docs):
    inverse_index = {}
    for doc, path in docs:
        for word in doc:
            if word not in inverse_index: inverse_index[word] = set()
            inverse_index[word].add(path)
    return inverse_index

def get_query_vector(query):
    query_vector = {}
    query = [morph.parse(word)[0].normal_form for word in query.lower().split()]


    C = {}
    for word in query:
        C[word] = C[word] + 1 if word in C else 1

    for word in query:
        if word not in query_vector:
            tf = C[word] * 1.0 / len(query)            
            query_vector[word] = tf


    return query_vector

def get_distance(v1, v2):
    def f(v):
        return sum([x**2 for x in v.values()])

    prod = sum([v1[word]*v2[word] for word in v1 if word in v2 ])

    return prod/math.sqrt(f(v1)*f(v2))

dir_with_docs = 'documents'

docs_path = [os.path.join(dir_with_docs, f) for f in os.listdir(dir_with_docs)]
docs = [(get_doc(path), path) for path in docs_path]
inverse_index = get_inverse_index(docs)
docs_vector = [(get_doc_vector(doc, inverse_index, len(docs)), path) for doc, path in docs]

query = sys.argv[1:len(sys.argv)]

if len(query) == 0:
    sys.exit('введите запрос')

query = ' '.join([word.decode('utf-8') for word in query])

query_vector = get_query_vector(query)

dist = [(path, get_distance(query_vector, doc_vector)) for doc_vector, path in docs_vector]



dist = sorted(filter(lambda x: x[1] != 0,dist), key=lambda x: x[1], reverse=True)

for a, b in dist:
    print '%f\t%s' % (b,a)