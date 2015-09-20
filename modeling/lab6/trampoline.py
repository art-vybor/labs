from math import sqrt

m = 80
k = 500
E_jump = 240
n = 10

g = 9.81

h = lambda dx: k*dx**2*1.0/(2*m*g)
new_dx = lambda dx: sqrt(dx**2+E_jump*2.0/k)

dx = 0
for i in range(1, n+1):
    dx = new_dx(dx)

    print 'h(%s) = %s' % (i, h(dx))



