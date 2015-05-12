import copy
from math import sqrt
import numpy

A = [[1,0,0],
     [0,1,0],
     [0,0,0]]
b = [1,2,1]
x = [1,2,1]

A1 = [[ 2, 1,-1],
      [-3,-1, 2],
      [-2, 1, 2]]
b1 = [8,-11,-3]
x1 = [2,  3,-1]

A2 =[[15, 2,-1,-1],
     [1,-10,-1,-2],
     [2,  1,12, 1],
     [1,  1, 1,11]]
b2 = [22,-14,-10,-20]
x2 = [1, 2,   -1, -2]

def gaussian(A, b):
    n = len(A)    
    x = [0]*n

    #A = A|b
    for i in range(n):
        A[i].append(b[i])

    for k in range(1, n):
        for j in range(k, n):
            m = A[j][k-1]*1.0 / A[k-1][k-1]
            for i in range(n+1):
                A[j][i] -= m*A[k-1][i]

    b = [A[i][len(A)] for i in range(len(A))]

    for i in range(n):
        if (sum(A[i][j] for j in range(n)) == 0) and b[i] != 0:
            print 'SLAE is inconsistent'
            return []

    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            b[i] -=A[i][j]*x[j]
        x[i] = b[i]*1.0 / A[i][i]
 
    return x


def seidel(A, b, eps):
    n = len(A)

    #M = -(L+D)^{-1}*U
    LD = copy.deepcopy(A)
    U  = copy.deepcopy(A)
    for i in range(n):
        for j in range(n):
            if j > i: LD[i][j] = 0
            else:     U[i][j] = 0
    M = -numpy.dot(numpy.linalg.inv(LD),U)
    if numpy.linalg.norm(M) >= 1:
        print 'SLAE is inconsistent'
        return []

    #Ax=b    
    x = [0] * n
    converge = False
    while not converge:
        p = copy.copy(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(i))
            s += sum(A[i][j] * p[j] for j in range(i+1,n))
            x[i] = (b[i] - s)*1.0 / A[i][i]
 
        converge = sqrt(sum((x[i]-p[i])**2 for i in range(n))) < eps
    return x

print seidel(A2, b2, 0.001)

#print gaussian(A1, b1)