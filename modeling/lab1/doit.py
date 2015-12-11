# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np
import random

train_size = 0.9
bins_for_histogram = 10

def build_probability_dict(f):
    P = {}
    for x in f:
        if x not in P:
            P[x] = 0
        P[x] += 1
    return {k:v*1.0/len(f) for k,v in P.iteritems()}
        
def M(X):
    P = build_probability_dict(X)
    return sum(x*p for x,p in P.iteritems())
    
def D(X):
    X_2 = [x**2 for x in X]
    return M(X_2) - M(X)**2


def train_model(f1, f2):
    beta = math.sqrt(D(f1)/D(f2))
    alpha = math.exp(M(f1) - beta*M(f2))
    return (alpha, beta)

def split(f):
    train_len = int(len(f)*train_size)
    if train_len == 0:
        train_len = 1
    if train_len == len(f):
        train_len = len(f) - 1
    return f[:train_len], f[train_len:]

def apply_model(model, f):
    alpha, beta = model
    return [alpha * x**beta for x in f]

def get_quality(f1, f2):
    def get_mean_for_interval(f, start, end):
        summ = 0
        num = 0
        for y in f:
            if start <= y and y < end:
                summ += y
                num += 1
        if num != 0:
            return summ*1.0/num
        return 0

    P1 = build_probability_dict(f1).values()    
    P2 = build_probability_dict(f2).values()
    start = 0.0
    n1 = []
    n2 = []
    for x in xrange(1, bins_for_histogram+1, 1):
        end = x*1.0/bins_for_histogram
        
        n1.append(get_mean_for_interval(P1, start, end))
        n2.append(get_mean_for_interval(P2, start, end))

        start=end

    return max(abs(np.array(n1) - np.array(n2)))

def case(f1, f2):
    divider = max(f1+f2)

    f1 = [x*1.0/divider for x in f1]
    f2 = [x*1.0/divider for x in f2]

    train1, test1 = split(f1)
    train2, test2 = split(f2)

    model = train_model(train1, train2)
    #print model
    alpha, beta = model

    test1_applied = apply_model(model, test1)

    return alpha, beta, get_quality(test2, test1_applied)

import pandas
oil = pandas.read_csv('oil.big', sep=' ')
rub = pandas.read_csv('rub_cutted', sep=' ')

oil = [float(x) for x in list(oil['cost'])]
rub = [float(x) for x in list(rub['Nominal']) if x != '—']

l = min(len(oil), len(rub))
oil = oil[:l]
rub = rub[:l]

random.shuffle(oil)
random.shuffle(rub)

# f = zip (oil, rub)
# x = []
# for a,b in f:
#     x.append(a*b)
# plt.plot(x)
# plt.show()

x = []
a = []
b = []
q = []
alpha, beta = 1,1
for s in xrange(1,100,1):
    train_size = s*1.0/100;
    x.append(train_size*len(rub))
    alpha, beta, qual = case(rub, oil)
    a.append(alpha)
    b.append(beta)
    q.append(qual)
    
print alpha, beta
# plt.plot(x,a)
# plt.plot(x,b)
plt.plot(x,q)
plt.show()
