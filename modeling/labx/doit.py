# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np
import random

# f1 = [random.randint(1, 10) for _ in xrange(100)]
# f2 = [random.randint(1, 10) for _ in xrange(100)]

train_size = 1
# bins_for_histogram = 100

def build_probability_dict(f):
    P = {}
    for x in f:
        if x not in P:
            P[x] = 0
        P[x] += 1

    return {k:v*1.0/len(f) for k,v in P.iteritems()}
        
def M(P):
    M = 0
    for k,v in P.iteritems():
        M += k*v
    return M

def D(f,M_f):
    g = [x**2 for x in f]
    R = build_probability_dict(g)
    return M(R) - M_f

def train_model(f1, f2):
    P1 = build_probability_dict(f1)
    P2 = build_probability_dict(f2)
    M1 = M(P1)
    M2 = M(P2)

    D1 = D(f1, M1)
    D2 = D(f2, M2)

    beta = math.sqrt(D1/D2)
    alpha = math.exp(M1 - beta*M2)
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

# def get_quality(f1, f2):
#     def get_mean_for_interval(f, start, end):
#         summ = 0
#         num = 0
#         for y in f:
#             if start <= y and y < end:
#                 summ += y
#                 num += 1
#         if num != 0:
#             return summ*1.0/num
#         return 0

#     P1 = build_probability_dict(f1).values()    
#     P2 = build_probability_dict(f2).values()
#     start = 0.0
#     n1 = []
#     n2 = []
#     for x in xrange(1, bins_for_histogram+1, 1):
#         end = x*1.0/bins_for_histogram
        
#         n1.append(get_mean_for_interval(P1, start, end))
#         n2.append(get_mean_for_interval(P2, start, end))

#         start=end

#     return max(abs(np.array(n1) - np.array(n2)))

def case(f1, f2):
    #print f1, f2
    divider = max(f1+f2)

    f1 = [x*1.0/divider for x in f1]
    f2 = [x*1.0/divider for x in f2]
    #print f1

    train1, test1 = split(f1)
    train2, test2 = split(f2)

    model = train_model(train1, train2)
    #print model
    alpha, beta = model

    #test1_applied = apply_model(model, test1)

    return alpha, beta #, get_quality(test2, test1_applied)

def get_data_by_column_name(data, column_name):
    col1 = data[column_name]
    col2 = data[column_name+'p']
    x3, x31, x32, x33 = [], [], [], []
    for i in range(0,len(col1),3):
        if not np.isnan(col1[i]):
            x3.append(col1[i])
            x31.append(col2[i])
            x32.append(col2[i+1])
            x33.append(col2[i+2])
    return x3, x31, x32, x33

import pandas
data = pandas.read_csv('data.csv')

# x3, x31, x32, x33 = get_data_by_column_name(data, 'IIB0')
# a1, b1 = case(x3, x31)
# print a1, b1

# import sys
# sys.exit(0)

for station in ['A0', 'A1', 'B0', 'B1', 'C0', 'C1']:
    print station, 
    x3, x31, x32, x33 = get_data_by_column_name(data, 'II' + station)
    a1, b1 = case(x3, x31)
    a2, b2 = case(x3, x32)
    a3, b3 = case(x3, x33)
    print a1, b1, a2, b2, a3, b3

x3, x31, x32, x33 = [], [], [], []
for station in ['A0', 'A1', 'B0', 'B1', 'C0', 'C1']:
    #print station, 
    _x3, _x31, _x32, _x33 = get_data_by_column_name(data, 'II' + station)
    x3.extend(_x3)
    x31.extend(_x31)
    x32.extend(_x32)
    x33.extend(_x33)

a1, b1 = case(x3, x31)
a2, b2 = case(x3, x32)
a3, b3 = case(x3, x33)
print a1, b1, a2, b2, a3, b3

x31.extend(x32)
x31.extend(x33)
print case(x3, x31)

# print case([1,2,3,4,5,6,7,8,9,10], [2,4,6,8,10,12,14,16,18,20])
# print apply_model((0.679, 1.118),[1,2,3,4,5,6,7,8,9,10])
# rub = pandas.read_csv('rub_cutted', sep=' ')

# oil = [float(x) for x in list(oil['cost'])]
# rub = [float(x) for x in list(rub['Nominal']) if x != '—']

#print oil
# random.shuffle(oil)
# random.shuffle(rub)

# x =[]
# a=[]
# b=[]
# q=[]
# for s in xrange(1,100,1):
#     train_size = s*1.0/100;
#     x.append(train_size)
#     alpha, beta, quality = case(oil, rub)
#     a.append(alpha)
#     b.append(beta)
#     q.append(quality)

# plt.plot(x,a)
# plt.plot(x,b)
# # plt.plot(x,q)
# plt.show()

# На основе полученных данных оценить среднюю стоимость поездки. Оценив, применимость обобщённой функции.