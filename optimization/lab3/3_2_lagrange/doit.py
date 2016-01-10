from scipy import optimize

r = 0.1
eps = 1e-9
C = 4
mu = (0, 0)

f = lambda (x1, x2): (x1**2 - 2)**2 + x2**2 - 1

g1 = lambda (x1, x2): -(x1+1)**2 + 3
g2 = lambda (x1, x2): (x1+x2)**2 - 2
g = [g1, g2]

P = lambda x, r: sum(max(0, mi + r * gi(x))**2 - mi**2 for mi, gi in zip(mu, g)) / (2*r)

L = lambda x, r: f(x) + P(x, r)

def F(x, rk):
    x = tuple(x)
    return f(x) + P(x, rk)

x = (0,0)
print 'x0: %s' % list(x)

while True:
    x = tuple(optimize.minimize(lambda x: F(x, r), x).x)
    print 'x = %s, penalty: %s, ' % (list(x), P(x, r))
    if not abs(P(x, r)) <= eps:
        mu = [max(0, mi+r*gi(x)) for mi, gi in zip(mu, g)]
        r *= C
    else:
        break

print 'result: %s' % list(x)
print 'f(result) = %s' % f(x)