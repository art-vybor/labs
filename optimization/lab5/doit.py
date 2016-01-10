# -*- coding: utf-8 -*-
from math import sin, sqrt
from random import random, uniform, randint
from copy import deepcopy

Np = 100 # размер популяции
F = 1 #100 # весовой коэффициент
CR = random() # параметр операции скрещивания
M = 1000 #2000 # максимальное количество популяций


#a, b, c = 0.5, 0.5, 0.5
#a, b, c = 1.0, 0.8, 1.0
a, b, c = 2.5, 1.0, 2.0

f = lambda (x1,x2): a*x1*sin(b*sqrt(abs(x1))) + x2*sin(c*sqrt(abs(x2)))
x_min = -500
x_max = 500

def normalize(x=None):
    if x < x_min or x_max < x:
        return uniform(x_min, x_max)
    return x

def getXc1(incorrect_index):
    Xabc = set()
    while not len(Xabc) == 3:
        index = randint(0, len(X)-1)
        if index != incorrect_index:
            Xabc.add(index)
    i, j, k = list(Xabc)
    Xa, Xb, Xc = X[i], X[j], X[k]

    return [normalize(Xc[0] + F*(Xa[0]-Xb[0])), normalize(Xc[1] + F*(Xa[1]-Xb[1]))]

def getXs(Xc1, Xt):
    Xs = deepcopy(Xc1)
    if random() > CR:
        Xs[0] = Xt[0]
    return Xs

X = [[normalize(), normalize()] for _ in range(Np)]

m = 0
for _ in range(M):
    X_new = []
    for j in range(Np):
        Xt = X[j]
        Xs = getXs(getXc1(j), Xt)

        X_new.append(Xs if f(Xs) < f(Xt) else Xt)
    X = X_new

print 'a = %s, b = %s, c = %s' % (a,b,c)
print 'f = %s, x = %s' % min((f(x), x) for x in X)