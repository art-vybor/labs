# -*- coding: utf-8 -*-

import numpy
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, rosen, rosen_der
from pybel import *

data = {
    'O=CO': {'pKa':3.75, 'name':'муравьиная'},
    'CC(O)=O': {'pKa':4.76, 'name':'уксусная'},
    'CCС(O)=O': {'pKa':4.88, 'name':'пропионовая'},
    'CCCCC(O)=O': {'pKa':4.82, 'name':'валериановая'},
    'C(Cl)C(=O)O': {'pKa':2.87, 'name':'монохлоруксусная'},
    'ClC(Cl)(Cl)C(O)=O': {'pKa':0.77, 'name':'трихлоруксусная'},
    'C(=O)(C(F)(F)F)O': {'pKa':0.23, 'name':'трифторуксусная'},
    'CC(O)C(=O)O': {'pKa':3.86, 'name':'молочная'},
    'C(=O)(C(=O)O)O': {'pKa':1.25, 'name':'щавелевая'},
}

field = 'pKa'

split_index = 5

train_set = {}
test_set = {}
i = 0
for smiles in data:
    if i < split_index:
        train_set[smiles] = data[smiles]
    else:
        test_set[smiles] = data[smiles]
    i+=1

features = [
    lambda x: len(filter(lambda c: c=='C', x)),
    lambda x: len(filter(lambda c: c=='l', x)),
    lambda x: len(filter(lambda c: c=='O', x)),
    lambda x: len(filter(lambda c: c=='F', x)),
    #lambda x: readstring('smi',x).molwt,
    lambda x: len(filter(lambda c: c=='=', x)),
]

def apply_features(smiles, features, model):
    return sum([f(smiles)*v for f, v in zip(features, model)])

def distance_set(A,B):
    return sum([abs(B[smiles][field] - A[smiles][field]) for smiles in A])

def train(dataset, features, model=[1,1,1,1,1]):
    def func_min(model):
        return distance_set(apply_model(dataset, features, model), dataset)

    model = minimize(func_min, model, method='Nelder-Mead')    

    return list(model.x)

def apply_model(dataset, features, model):    
    applied = {}
    for smiles in dataset:
        applied[smiles] = {field: apply_features(smiles, features, model)}
    return applied

def evaluate(dataset, predicted_set):
    return distance_set(dataset, predicted_set) #/ sum([predicted_set[smiles]['lambda'] for smiles in predicted_set])

def draw(dataset, type='o'):
    x = []
    y = []
    i = 0
    for smiles in dataset:
        x.append(i)
        y.append(dataset[smiles][field])
        i+=1
    
    plt.axis([0, i, 0, 10])
    plt.plot(x,y,'o')    

model = train(train_set, features)
print 'model', model
applied = apply_model(test_set, features, model)
print 'apply', applied
print 'evaluate', evaluate(test_set, applied)
print 'evaluate random', evaluate(apply_model(test_set, features, [1,1,1,1,1]), applied)
draw(test_set)
draw(applied)
plt.show()
plt.clf()