import math
import numpy as np
import matplotlib.pyplot as plt

l = 1
k = 3
step = 1e-2

integral = lambda f: sum(f(x)*step for x in np.arange(0,l,step))

u = lambda x: x*x*math.log(x+1)
f = lambda x: 2*math.log(x+1) + 4*x*1.0/(x+1) - x**2*1.0/(x+1)**2

phi_0 = lambda x: l*math.log(l+1)*1.0*x
phi_i = lambda i: lambda x: math.sin(math.pi * i * x * 1.0/ l)
phi = [phi_0] + [phi_i(i) for i in range(1,k+1)]

a = lambda i: - (i*math.pi)**2 / (2*l)
b_f = lambda x, i: f(x) * phi_i(i)(x)
b = lambda i: integral(lambda x: b_f(x, i))
c = [1] + [b(i)*1.0/a(i) for i in range(1,k+1)]

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
