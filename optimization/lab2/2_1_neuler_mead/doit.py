from math import sqrt

alpha = 1
beta = 0.5
gamma = 2

n = 2
eps = 1e-9

f = lambda (x1, x2): 2*x1*x1 + x1*x2 + x2*x2 - 6*x1 - 5*x2


def get_xc(x):
    return [sum(x[i][j] for i in range(n)) *1.0 / n for j in range(n)]

def get_xr(xc, xh):
    return [(1+alpha)*xc[i] - alpha*xh[i] for i in range(n)]

def diff(xs, x2):
    fx2 = f(x2)
    return sqrt(abs(sum(f(x) - fx2 for x in xs)*1.0 / (n + 1)))

def nelder_mead(x):    
    while True:
        # stage 2: sort 
        x = sorted(x, key=lambda x: f(x))
        l = 0 # lowest
        g = 1 # second greatest
        h = 2 # greatest

        # stage 3: get centroid of first n points
        xc = get_xc(x)

        # stage 4: reflect xh point from xc
        xr = get_xr(xc, x[h]);

        # stage 5: compare f(xi)
        if f(xr) < f(x[l]):
            xe = [(1-gamma)*xc[i]+gamma*xr[i] for i in range(n)] #tension
            x[h] = xe if f(xe) < f(xr) else xr
            break #goto 9        

        if f(x[l]) < f(xr) and f(xr) < f(x[g]):
            x[h] = xr
            break #goto 9

        if f(x[g]) < f(xr) and f(xr) < f(x[h]):
            xr, x[h] = x[h], xr
        
        # stage 6: compress
        xs = [beta*x[h][i] + (1-beta)*xc[i] for i in range(n)]

        #stage 7
        if f(xs) <= f(x[h]):
            x[h] = xs
            break #goto 9        

        #stage 8
        else:
            for k in [1,2]:
                x[k] = [x[l][i] + (x[k][i] - x[l][i])/2.0 for i in range(n)]

        break #goto 9

    # stage 9
    if diff(x, get_xc(x)) < eps:
        return x[l]

    return nelder_mead(x)


# stage 1: select n+1 points
points = [[1,0], [0,1], [1,1]]

print nelder_mead(points)

print 13.0/7, 11.0/7