import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import pandas

bins_for_histogram = 20

def get_quality(f1, f2):
    def get_mean_for_interval(f, start, end, first=False):
        summ = 0
        num = 0
        for y in f:
            if start < y and y <= end:
                summ += y
                num += 1

            if first and start == y:
                summ += y
                num += 1
        if num != 0:
            return summ*1.0/num
        return 0

    P1 = f1
    P2 = f2 
   
    start = min(min(P1), min(P2))
    end = max(max(P1), max(P2))    
    step = (end-start)/(bins_for_histogram+1)
    prev_start = start
    start += step
    n1 = []
    n2 = []
    first = True
    while start <= end:
        #print prev_start, start
        n1.append(get_mean_for_interval(P1, prev_start, start, first))
        n2.append(get_mean_for_interval(P2, prev_start, start, first))
        first = False
        #print n2

        prev_start = start
        start += step
    return n1, n2, sum(abs(np.array(n1) - np.array(n2)))


metro = pandas.read_csv('data_praga_metro_1.csv', sep=',')
stations = ['A0', 'A1', 'B0', 'B1', 'C0', 'C1']

total_a = []
total_b =[]
for station in stations:
    a = [float(x) for x in list(metro['th'+station])]
    b = [float(x) for x in list(metro['r'+station])]
    total_a.extend(a) 
    total_b.extend(b)

divider = max(total_a+total_b)

total_a = [x*1.0/divider for x in total_a]
total_b = [x*1.0/divider for x in total_b]

a_60,b_60 = [],[]
f = []
for i in range(0, len(total_a)-1):
    a = total_a[:i] + total_a[i+1:]
    b = total_b[:i] + total_b[i+1:]
    if i == 60:
        a_60 = a
        b_60 = b
    x,y,q = get_quality(a, b)
    f.append(q)

    print int(a[i]*divider), int(b[i]*divider), q 

print 'min', min(f)
print 'max', max(f)
print total_a[60]*divider, total_b[60]*divider


def draw(a,b):
    def add_plot(a, clr):
        x,y=[],[]
        i = 0
        while i < len(a):
            x.append(i)
            x.append(i+1)
            y.append(a[i])
            y.append(a[i])
            i+=1
            plt.plot(x,y,color=clr)
            x,y = [],[]
            
    add_plot(a,'b')
    add_plot(b,'g')
    plt.show()

x,y,q = get_quality(total_a, total_b)
print 'total:',q
draw(x,y)

x,y,q = get_quality(a_60, b_60)
print 'total:',q
draw(x,y)