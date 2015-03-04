import numpy
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, rosen, rosen_der
from pybel import *

print readstring('smi','c1ccccc1').molwt
#
data = {
    'c1ccccc1': {'lambda':255, 'name':'Benzene'},
    'c1cccc2c1cccc2': {'lambda':275, 'name':'Naphthalene'},
    'c3ccc2cc1ccccc1cc2c3': {'lambda':370, 'name':'Anthracene'},
    'c34cc2cc1ccccc1cc2cc3cccc4': {'lambda':460, 'name':'Tetracene'},
    'c1ccc2cc3cc4cc5ccccc5cc4cc3cc2c1': {'lambda':580,'name':'pentacene'},
    'C1=CC=C2C=C3C=C4C=C5C=C6C=CC=CC6=CC5=CC4=CC3=CC2=C1'.lower(): {'lambda':693,'name':'hexacene'},
    'c1ccc5cccc4c5c1c2cccc3cccc4c23': {'lambda':432,'name':'perylene'},
    'c1ccccc1(c2ccccc2)': {'lambda':251.5, 'name':'bifenil'},

}

test = {
    
    'c1cc2ccc3ccc4ccc5ccc6ccc1c7c2c3c4c5c67': {'lambda':411,'name':'coronene'},
    #'c1ccc5cccc4c5c1c2cccc3cccc4c23': {'lambda':432,'name':'perylene'},
    #'': {'lambda':291, 'name':'binaftil'},
    #'': {'lambda':267, 'name':'digidrofenatren'},



}

features = [
    lambda x: len(filter(lambda c: c=='c', x)),
    lambda x: len(filter(lambda c: c=='1', x)),
    lambda x: len(filter(lambda c: c=='2', x)),
    #lambda x: readstring('smi',x).molwt,
    lambda x: len(filter(lambda c: c.isdigit(), x)),
    lambda x: len(x),
]

x0=[1,1,1,1,1]

z = []

def d(vect, smiles):
    d = 0
    for i in range(len(features)):
        d += features[i](smiles)*vect[i]
    return d

def f(z, x):
    return z[0]*x+z[1]

def r(vect):
    r = 0 
    for mol in data:
        r += (f([1,1], d(vect, mol)) - data[mol]['lambda'])**2
    return r

def draw(x0):
    global z
    table_d_lambda = {}
    for mol in data:
        table_d_lambda[d(x0, mol)] = data[mol]['lambda']

    x = table_d_lambda.keys()
    print 'd (lambda) = ', x
    y = table_d_lambda.values()
    print 'lambda = ', y
    # plot the data itself
    pylab.plot(x, y, 'o')
    # calc the trendline (it is simply a linear fitting)
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    pylab.plot(x,p(x),'r-')

    # the line equation:
    print 'y=%.6fx+(%.6f)'%(z[0],z[1])

    plt.plot(x,y,'o')
    #plt.show()
    plt.clf()
draw(x0)

print 'r = ', r(x0)

res = minimize(r, x0, method='Nelder-Mead')

print 'minimize r = ', r(res.x)
print 'res.x = ', res.x
draw(res.x)

x = []
y = []
#test
vect = res.x
test_set = data

# for a in test:
#     test_set[a] = test[a]

r = 0 
for mol in test_set:
    print test_set[mol]['name'], test_set[mol]['lambda'], f(z, d(vect, mol))
    y.append(test_set[mol]['lambda'])
    x.append(f(z, d(vect, mol)))

    r += (f(z, d(vect, mol)) - test_set[mol]['lambda'])**2
print 'OPTIMIZE R: ', r

_x = []
_y = []
for mol in test:
    print 'test: ', test[mol]['lambda'], f(z, d(vect, mol))
    _y.append(test[mol]['lambda'])
    _x.append(f(z, d(vect, mol)))
plt.plot(_x,_y,'go')

#test_random
vect = x0
r = 0 
for mol in test_set:
    r += (f(z, d(vect, mol)) - test_set[mol]['lambda'])**2
print 'random R: ', r




z = numpy.polyfit(x, y, 1)
p = numpy.poly1d(z)
pylab.plot(x,p(x),'r-')
plt.plot(x,y,'o')
plt.show()