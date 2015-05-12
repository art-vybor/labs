from functools import partial

import numpy as np
from numpy import linalg

from sympy import symbol, diff, Matrix, N
from sympy.parsing.sympy_parser import parse_expr


#F(x,y) = 0
F = map(parse_expr, 
            ['x**2 + x - y**2 - 0.15', 
             'x**2 - y + y**2 + 0.17'])
q = [0, 0] #[0.2, 0.3]

F1 = map(parse_expr, 
            ['x + 3*log(x,10) - y**2', 
             '2*x**2 - x*y - 5*x + 1'])
q1 = [3.5, 2.2] #[3.48, 2.26]

#fixed_point x = f1(x,y), y = f2(x,y)
F2 = map(parse_expr, 
            ['-0.1*x**2 - 0.2*y**2 + 0.3', 
             '-0.2*x**2 + 0.1*x*y + 0.7'])
q2 = [0.25, 0.75]

x, y = symbol.symbols('x y')


def subs_2d(F, q):
    return map(lambda f: f.subs(x, q[0]).subs(y, q[1]).evalf(), F)


def subs_3d(W, q):
    return [subs_2d(W[0], q), subs_2d(W[1], q)]


def jacobian(F):
    return [[diff(F[0], x), diff(F[0], y)],
            [diff(F[1], x), diff(F[1], y)]]


def newton(F, q, eps):        
    W = jacobian(F)
    dx = [10**9, 10**9]
    result = q

    converge = False
    while not converge:
        F_subs = subs_2d(F, result)
        W_subs = subs_3d(W, result)

        #Wdx=-F
        dx = linalg.solve(np.array(W_subs), -np.array(F_subs))
        result = np.add(result, dx)

        converge = linalg.norm(dx) < eps
    return list(result)

def fixed_point(F, q, eps):
    previous = q
    converge = False
    while not converge:
        result = subs_2d(F, previous)
        result = map(float, result)
        
        print previous, result
        delta = np.subtract(result, previous)
        previous = result

        converge = linalg.norm(delta) < eps
    return result

#print newton(F1, q1, 0.1)
print fixed_point(F2, q2, 0.000001)