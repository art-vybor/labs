import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative

l = 1
k = 10
step = 1e-2

integral = lambda f: sum(f(x)*step for x in np.arange(0,l,step))

#plus = lambda t, r: t**r if t > 0 else 0


delta = l*1.0/k
base = [i*delta for i in range(k+1)]

t = [None] + [base[0]-delta] + base + [base[-1]+delta]
#t = [None] + [i*delta for i in range(k+4)]
print t

def B_in(i,n,x):
#    print i,n,x
    if n == 1:
        return 1 if t[i] <= x and x < t[i+1] else 0
    else:
        return (x-t[i])*1.0 / (t[i+n-1]-t[i]) * B_in(i,n-1,x) + \
            (t[i+n]-x)*1.0 / (t[i+n]-t[i+1]) * B_in(i+1,n-1,x)

B_3 = lambda x: \
    (plus(x+2,3) - 4*plus(x+1,3) + 6*plus(x,3) - 4*plus(x-1,3) + plus(x-2, 3)) * 1.0/6

# B_3 = lambda i,x: \
#      (plus(t[i-1]-x,3) - 4*plus(t[i+2]-x,3) + 6*plus(t[i+3]-x,3) - 4*plus(t[i+4]-x,3) + plus(t[i+5]-x, 3)) * 1.0/6/h**4

u = lambda x: x*x*math.log(x+l)
f = lambda x: 2*math.log(x+l) + 4*x*1.0/(x+l) - x**2*1.0/(x+l)**2
g = lambda x: 2*x*math.log(x+l) + x**2*1.0/(x+l)

phi_0 = lambda x: l*math.log(2*l)*1.0*x
phi_i = lambda i: lambda x: B_in(i,3,x)*(x-l)*x
#phi_i = lambda i: lambda x: B_3((x+math.pi)/h-i)
phi = [phi_0] + [phi_i(i) for i in range(1,k+1)]


for i in range(1, k+1):
    X = np.arange(0,l,step)
    Y = [phi_i(i)(x) for x in X]
    plt.plot(X, Y,label=i)
plt.legend()
plt.show()

import sys
#sys.exit(0)
def a_ij(i,j):
    #return integral(lambda x: (phi_i(i)(x)) * phi_i(j)(x))
    return integral(lambda x: derivative(phi_i(i), x, 1e-7,n =2) * phi_i(j)(x))
    #return integral(lambda x: B_in(i,2,x) * phi_i(j)(x))


a = [None]*(k)
for i in range(1,k+1):
    a[i-1] = [a_ij(i,j) for j in range(1, k+1)]


#b_f = lambda x, i: 
def b_f(x,i):
    #print x, i, phi_i(i)(x)
    return f(x) * phi_i(i)(x)
b = lambda i: integral(lambda x: b_f(x, i))

#c = [1] + [b(i)*1.0/a(i) for i in range(1,k+1)]


a = np.array(a)

b  = np.array([b(i) for i in range(1, k+1)])

print 'a=',a
print 'b=',b

c = np.linalg.solve(a,b)

#print c
c = [1] + list(c)
print 'c=',c

um = lambda x: sum(c[i]*phi[i](x) for i in range(0,k+1)) #- sum(c[i]*phi[i](0) for i in range(0,k+1))

N = sum((u(x) - um(x))**2 for x in np.arange(0,l,step))

print 'residual: ', N

def draw(f, label, draw_type):
    x = np.arange(0,l,step)
    y = map(f, x)
    plt.plot(x, y, draw_type,label=label)

# print u(0)- um(0)
# print u(l)- um(l)
draw(u, 'u', '')
draw(um, 'um', 'p')

plt.legend()
plt.show()
