from math import sqrt
import numpy as np
from copy import deepcopy

n = 2
eps = 1e-9
gamma = 10e4
alpha = 1
M = 10000

f = lambda (x1, x2): 2*x1*x1 + x1*x2 + x2*x2 - 6*x1 - 5*x2
grad = lambda (x1, x2): [4*x1 + x2 - 6, x1 + 2*x2 - 5]
H = [[4,1],
     [1,2]]


def H_plus_ykE(gamma):
    return [[4+gamma,1],
            [1,2+gamma]]

def mul(H, x):
    return [sum([ H[i][j] * x[j] for j in range(n)]) for i in range(n)]



xk = [0, 0]
k = 0

while np.linalg.norm(grad(xk)) > eps and k < M:
    dk = map(lambda x: -x, mul( np.linalg.inv(H_plus_ykE(gamma)), grad(xk)))

    xn = [xk[i] + alpha*dk[i] for i in range(n)]

    if f(xn) < f(xk):
        k += 1
        gamma /= 2
    else:
        gamma *= 2
    xk = xn

print '%s in %s iteration' % (xk, k)
print 'f = %s' % (f(xk))
