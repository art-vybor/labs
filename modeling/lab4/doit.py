import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import pandas

bins_for_histogram = 20
def build_probability_dict(f):
    P = {}
    for x in f:
        if x not in P:
            P[x] = 0
        P[x] += 1

    return {k:v*1.0/len(f) for k,v in P.iteritems()}


def get_quality(f1, f2):
    def get_mean_for_interval(f, start, end, first=False):

        #print f, start, end
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

    P1 = build_probability_dict(f1).values()    
    P2 = build_probability_dict(f2).values()
    
    start = min(min(P1), min(P2))
    end = max(max(P1), max(P2))    
    step = (end-start)/(bins_for_histogram+1)
    prev_start = start
    start += step

    #print start, end


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
    print n1
    print n2
    return max(abs(np.array(n1) - np.array(n2)))


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

# total_a = [x*1.0/divider for x in total_a]
# total_b = [x*1.0/divider for x in total_b]

for i in range(0, len(total_a)-1):
    a = total_a[:i] + total_a[i+1:]
    b = total_b[:i] + total_b[i+1:]
    #print i, get_quality(a, b)

print get_quality(total_a, total_b)