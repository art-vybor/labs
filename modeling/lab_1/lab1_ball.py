from math import pi, sin, cos, sqrt
import matplotlib.pyplot as plt
import numpy as np

consts = {
    'alpha': pi/4,
    'v0': 50.0,
    'r': 0.1,
    'g': 9.80665,
    'C': 0.15, #coefficient of drag
    'air_density': 1.225,
    'lead_density': 11340,
    'dx': 0.001,    
    'dt': 0.001,
}


def plot(x, y, label, color=''):
    plt.plot(x, y, color, label=label)
    plt.title('modeling lab1')
    plt.ylabel('y')
    plt.xlabel('x')
    plt.ylim([0,70])

def galilei(label='Galilei', alpha=None, v0=None, x0=None, g=None, dx=None, **args):
    print label

    vx, vy = v0*cos(alpha), v0*sin(alpha)

    # x = vx*t => t = x/vx
    t = lambda x: x / vx
    # y = vy*t - g*t**2/2 => y = vy*x/vx - g*x**2/(2 * vx**2)
    y = lambda x: vy * x / vx - g * x**2 / (2 * vx**2)

    x_vect, y_vect = [], []

    x = 1e-9
    while y(x) >= 0:
        x_vect.append(x)
        y_vect.append(y(x))
        x += dx

    print '\tlength: ', x
    print '\ttime: ', t(x)
    plot(x_vect, y_vect, label, 'r--')


def newton(label='Newton', alpha=None, v0=None, g=None, C=None, air_density=None, lead_density=None, r=None, dt=None, **args):
    def runge_kutta_iteration(f, x, y, h):
        k1 = f(x, y)
        k2 = f(x+h/2, y+h*k1/2)
        k3 = f(x+h/2, y+h*k2/2)
        k4 = f(x+h, y+h*k3)

        return y + h/6*(k1+2*k2+2*k3+k4)

    print label

    m = lead_density * 4/3 * pi * r**3
    betta = 0.5 * C * pi*r**2 *air_density

    # F1x = -betta * vx * sqrt(vx**2 + vy**2)
    # F1y = -betta * vy * sqrt(vx**2 + vy**2)
    # F2y = -mg
    # ma = F1+F2

    vx, vy = v0*cos(alpha), v0*sin(alpha)

    dvx_dt = lambda vy, vx: -betta*vx*sqrt(vx**2+vy**2)/m
    dvy_dt = lambda vx, vy: -g-betta*vy*sqrt(vx**2+vy**2)/m

    x_vect, y_vect = [], []    

    x, y = 0, 0
    i = 0

    while y >= 0:
        #print x, y, vx, vy
        vx, vy = runge_kutta_iteration(dvx_dt, vy, vx, dt), \
                    runge_kutta_iteration(dvy_dt, vx, vy, dt) 
        x += vx*dt
        y += vy*dt
        x_vect.append(x)
        y_vect.append(y)

        i += 1

    print '\tlength: ', x
    print '\ttime: ', i*dt
    plot(x_vect, y_vect, label)
    
 

galilei(**consts)
newton(**consts)
consts['C']=0
newton(label='Newton without drag', **consts)
plt.legend()
plt.show()