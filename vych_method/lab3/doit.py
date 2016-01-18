from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import itertools

    
a,b,c,d = 4.5,2.5,None,1
R = b-d
step = 0.2

union = lambda f, g: lambda x, y: f(x, y) + g(x, y) + sqrt(f(x, y)**2 + g(x, y)**2)
intersect = lambda f, g: lambda x, y: f(x, y) + g(x, y) - sqrt(f(x, y)**2 + g(x, y)**2)
no = lambda f: lambda x,y: -f(x,y)

line = lambda value: value + abs(value)
circle = lambda R, x_0, y_0: lambda x, y: (R**2-(x-x_0)**2-(y-y_0)**2) / 2*R

z1 = lambda x,y: (a**2-x**2) / (2*a)
z2 = lambda x,y: (b**2-y**2) / (2*b)
z3 = circle(R, 0, b) 
z4 = circle(R, 0, -b)

F =  intersect(intersect(z1, z2), no(union(z3,z4)))
U = lambda x, y: np.sign(x) if F(x,y) <= 0 else 0


# Draw
xy_size = 6
z_size = 2
X = np.arange(-xy_size, xy_size, step)
Y = np.arange(-xy_size, xy_size, step)
X, Y = np.meshgrid(X, Y)

def draw(Z):
    ax  = plt.figure().gca(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_zlim(-z_size, z_size)
    
    ax.contourf(X, Y, Z, cmap=cm.coolwarm)
    plt.show()

draw([[max(F(x,y),0) for x,y in zip(x,y)] for x, y in zip(X, Y)])
draw([[U(x,y) for x,y in zip(x,y)] for x, y in zip(X, Y)])