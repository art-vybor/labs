import numpy as np
from scipy.optimize import fsolve


m = 80
k = 5000
E_jump = 240
n = 20

g = 9.81

f = lambda x: -1/(x-1) + k - 1
F = lambda dx, dx1: f(dx1)*dx1**2 - f(dx)*dx**2 - 2*E_jump

h = lambda dx: k*dx**2*1.0/(2*m*g)
new_dx = lambda dx: min(fsolve(lambda dx1: F(dx, dx1), max(dx, 1e-5))[0], 1-1e-5)

dx = 0
for i in range(1, n+1):
    dx = new_dx(dx)

    print '(%s,%s)' % (i, h(dx))