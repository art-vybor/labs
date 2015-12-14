import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import pandas

def build_probability_dict(f):
    P = {}
    for x in f:
        if x not in P:
            P[x] = 0
        P[x] += 1

    return {k:v*1.0/len(f) for k,v in P.iteritems()}
        
def M(X):
    P = build_probability_dict(X)

    M = 0
    for k,v in P.iteritems():
        M += k*v
    return M

def D(X):
    X_2 = [x**2 for x in X]
    return M(X_2) - M(X)**2

def cov(X,Y):
    XY = [x*y for x,y in zip(X,Y)]
    return M(XY) - M(X)*M(Y)

def norm(f1,f2):
    divider = max(f1+f2)

    f1 = [x*1.0/divider for x in f1]
    f2 = [x*1.0/divider for x in f2]

    return f1, f2

def get_rank_table(X):
    start, end = min(X), max(X)
    step = (end - start)/9

    rank_X = {x: int((x - start)/step + 1) for x in X}
    return [rank_X[x] for x in X]

def rank_spirmen(X,Y):
    rank_X = get_rank_table(X)
    rank_Y = get_rank_table(Y)

    sum_d = [(x-y)**2 for x,y in zip(rank_X, rank_Y)]
    return 1 - 6.0*sum(sum_d)/(len(X)**3 - len(X))

def linear_pirson(X,Y):
    return cov(X,Y)*1.0/(math.sqrt(D(X))*math.sqrt(D(Y)))

def rank_pirson(X,Y):
    rank_X = get_rank_table(X)
    rank_Y = get_rank_table(Y)
    return sum([(x-y)**2*1.0/y for x,y in zip(rank_X, rank_Y)])


metro = pandas.read_csv('data_praga_metro_1.csv', sep=',')
stations = ['A0', 'A1', 'B0', 'B1', 'C0', 'C1']


total_a = []
total_b =[]
for station in stations:
    print station
    a = [float(x) for x in list(metro['th'+station])]
    b = [float(x) for x in list(metro['r'+station])]
    total_a.extend(a) 
    total_b.extend(b) 
    #a,b = norm(a,b)

    print 'linear_pirson: ', linear_pirson(a,b)
    print 'rank_pirson: ', rank_pirson(a,b)
    print 'rank_spirmen: ', rank_spirmen(a,b)

print '-------\ntotal:'
print 'linear_pirson: ', linear_pirson(total_a,total_b)
print 'rank_pirson: ', rank_pirson(total_a, total_b)
print 'rank_spirmen: ', rank_spirmen(total_a, total_b)
