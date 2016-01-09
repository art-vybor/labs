# penalty method

from scipy import optimize

r = 1e-5
eps = 1e-9
C = 4

f = lambda (x1, x2): (x1**2 - 2)**2 + x2**2 - 1

g1 = lambda (x1, x2): -(x1+1)**2 + 3
g2 = lambda (x1, x2): (x1+x2)**2 - 2
g = lambda g_j, x: max(g_j(x), 0)

P = lambda x, r: r*1.0/2 * (g(g1, x)**2 + g(g2, x)**2)

F = lambda x, r: f(x) + P(x, r)

def F(x, rk):
    x = tuple(x)
    return f(x) + P(x, rk)

x = (0,0)
print 'x0: %s' % list(x)

while True:
    x = tuple(optimize.minimize(lambda x: F(x, r), x).x)
    print 'x = %s, penalty: %s, ' % (list(x), P(x, r))
    if not P(x, r) <= eps:
        r *= C
    else:
        break

print 'result: %s' % list(x)
print 'f(result) = %s' % f(x)