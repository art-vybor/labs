import numpy
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, rosen, rosen_der
from pybel import *

mol = readstring('smi','c1ccccc1')
print mol
#
data = {
    'c1ccccc1': {'lambda':255, 'name':'Benzene'},
    'c1cccc2c1cccc2': {'lambda':275, 'name':'Naphthalene'},
    'c3ccc2cc1ccccc1cc2c3': {'lambda':370, 'name':'Anthracene'},
    'c34cc2cc1ccccc1cc2cc3cccc4': {'lambda':460, 'name':'Tetracene'},
    'c1ccc2cc3cc4cc5ccccc5cc4cc3cc2c1': {'lambda':580,'name':'pentacene'},
    'C1=CC=C2C=C3C=C4C=C5C=C6C=CC=CC6=CC5=CC4=CC3=CC2=C1': {'lambda':693,'name':'hexacene'},
    'c1ccc5cccc4c5c1c2cccc3cccc4c23': {'lambda':432,'name':'perylene'},
    'c1ccccc1(c2ccccc2)': {'lambda':251.5, 'name':'bifenil'},
    'C=CC(=CCCC(=CC=CC(=CC=CC(=CC=CC=C(C)C=CC=C(C)C=CC=C(C)CCC=C(C)C)C)C)C)C=C': {'lambda':506, 'name':'Lycopene'},
    'c1cc2ccc3ccc4ccc5ccc6ccc1c7c2c3c4c5c67': {'lambda':411,'name':'coronene'}
}

new_data = {}
for smiles in data:
    mol = readstring('smi', smiles)
    mol.make3D()
    new_data[mol.write('smi').lower()] = data[smiles]

data =  new_data

split_index = 8

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
    lambda x: len(filter(lambda c: c=='c', x)),
    lambda x: len(filter(lambda c: c=='@', x)),
    lambda x: len(filter(lambda c: c=='1', x)),
    lambda x: len(filter(lambda c: c=='2', x)),
    #lambda x: readstring('smi',x).molwt,
    lambda x: len(filter(lambda c: c.isdigit(), x)),
]

def apply_features(smiles, features, model):
    return sum([f(smiles)*v for f, v in zip(features, model)])

def distance_set(A,B):
    return sum([abs(B[smiles]['lambda'] - A[smiles]['lambda']) for smiles in A])

def train(dataset, features, model=[1,1,1,1,1]):
    def func_min(model):
        return distance_set(apply_model(dataset, features, model), dataset)

    model = minimize(func_min, model, method='Nelder-Mead')    

    return list(model.x)

def apply_model(dataset, features, model):    
    applied = {}
    for smiles in dataset:
        applied[smiles] = {'lambda': apply_features(smiles, features, model)}
    return applied

def evaluate(dataset, predicted_set):
    return distance_set(dataset, predicted_set) #/ sum([predicted_set[smiles]['lambda'] for smiles in predicted_set])

def draw(dataset, type='o'):
    x = []
    y = []
    i = 0
    for smiles in dataset:
        x.append(i)
        y.append(dataset[smiles]['lambda'])
        i+=1
    
    plt.axis([0, i, 0, 700])
    plt.plot(x,y,'o')    

model = train(train_set, features)
applied = apply_model(test_set, features, model)
print 'apply', applied
print 'evaluate', evaluate(test_set, applied)
print 'evaluate random', evaluate(apply_model(test_set, features, [1,1,1,1,1]), applied)
draw(test_set)
draw(applied)
#plt.show()
#plt.clf()