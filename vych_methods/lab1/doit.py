from scipy import optimize
import numpy as np


x0=[0.0,0.0,0.0]

def f(l):
    x1,x2,x3 = l
    return x1*x1*x1 + x2*x2+x3*x3-3*x1+x2*x3+6*x2+2
    #return np.float64(x1)

f_min = optimize.minimize(f,x0)
print f_min.x, f_min.fun
f_max = optimize.minimize(lambda x: -f(x),x0)
print f_max.x, f_max.fun