import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative

l = 1
k = 10
step = 1e-2

integral = lambda f: sum(f(x)*step for x in np.arange(0,l,step))

delta = l*1.0/k
base = [i*delta for i in range(k+1)]
t = [None] + [base[0]-delta] + base + [base[-1]+delta]

def B_in(i,n,x):
    if n == 1:
        return 1 if t[i] <= x and x < t[i+1] else 0
    else:
        return (x-t[i])*1.0 / (t[i+n-1]-t[i]) * B_in(i,n-1,x) + \
            (t[i+n]-x)*1.0 / (t[i+n]-t[i+1]) * B_in(i+1,n-1,x)

u = lambda x: x*x*math.log(x+l)
f = lambda x: 2*math.log(x+l) + 4*x*1.0/(x+l) - x**2*1.0/(x+l)**2

phi_0 = lambda x: l*math.log(2*l)*1.0*x
phi_i = lambda i: lambda x: B_in(i,3,x)*(x-l)*x
phi = [phi_0] + [phi_i(i) for i in range(1,k+1)]

a_ij = lambda i,j: integral(lambda x: derivative(phi_i(i), x, 1e-7,n =2) * phi_i(j)(x))
a = [[a_ij(i,j) for j in range(1, k+1)] for i in range(1,k+1)]
b_f = lambda x, i: f(x) * phi_i(i)(x)
b = lambda i: integral(lambda x: b_f(x, i))

a = np.array(a)
b  = np.array([b(i) for i in range(1, k+1)])
c = np.linalg.solve(a,b)
c = [1] + list(c)

um = lambda x: sum(c[i]*phi[i](x) for i in range(0,k+1))

N = sum((u(x) - um(x))**2 for x in np.arange(0,l,step))

print 'residual: ', N

def draw(f, label, draw_type):
    x = np.arange(0,l,step)
    y = map(f, x)
    plt.plot(x, y, draw_type,label=label)

draw(u, 'u', '')
draw(um, 'um', 'p')

plt.legend()
plt.show()

# for i in range(1, k+1):
#     X = np.arange(0,l,step)
#     Y = [phi_i(i)(x) for x in X]
#     plt.plot(X, Y,label=i)
# plt.legend()
# plt.show()
