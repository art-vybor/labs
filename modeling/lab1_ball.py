from math import pi, sin, cos, sqrt
import matplotlib.pyplot as plt
import numpy as np

consts = {
    'alpha': pi/4,
    'v0': 50.0,
    'r': 0.1,
    'g': 9.80665,
    'x_step': 0.01,
    'x0': 0.000001,
    'C': 0.15, #coefficient of drag
    'air_density': 1.225,
    'lead_density': 4.53,
}


def plot(x, y, title):
    plt.plot(x, y)
    plt.title(title)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.show()
    plt.clf()    


def galilei(alpha=None, v0=None, x0=None, g=None, x_step=None, **args):
    print 'galilei'

    vx = v0*cos(alpha)
    vy = v0*sin(alpha)
    # x = vx*t => t = x/vx
    def t(x): return x / vx
    # y = vy*t - g*t**2/2 => y = vy*x/vx - g*x**2/(2 * vx**2)
    def y(x): return vy * x / vx - g * x**2 / (2 * vx**2)

    x_vect = []
    y_vect = []

    x = x0
    while y(x)>0:
        x_vect.append(x)
        y_vect.append(y(x))
        x += x_step

    print '\tlength: ', x
    print '\ttime: ', t(x)
    plot(x_vect, y_vect, 'galilei')


def newton(alpha=None, v0=None, x0=None, g=None, x_step=None, C=None, air_density=None, lead_density=None, **args):
    print 'newton'

    m = lead_density * 4/3 * pi * r**3
    betta = 0.5 * C * pi*r**2 *air_density
    
    #Fx = -betta * vx * sqrt(vx**2 + vy**2)
    #Fy = -betta * vy * sqrt(vx**2 + vy**2)

#galilei(**consts)