m = 80
k = 500
F_jump = 240
n = 10

g = 9.81

h = lambda dx: k*dx**2*1.0/(2*m*g)
new_dx = lambda dx, F_jump: dx+F_jump*1.0/k


dx = 0
for i in range(1,n+1):
    dx = new_dx(dx, F_jump)

    print 'h(%s) = %s' % (i, h(dx))

