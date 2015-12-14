# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


def kmeans(X, k):
    def equal(a,b):
        return set([tuple(x) for x in a]) == set([tuple(x) for x in b])

    def clusterize(X, centers):
        clusters  = defaultdict(list)
        for x in X:
            cluster_index = min([(i[0], np.linalg.norm(x-centers[i[0]])) \
                        for i in enumerate(centers)], key=lambda t:t[1])[0]

            clusters[cluster_index].append(x)
        return clusters
    
    def get_centers(clusters):
        centers = []
        for k in sorted(clusters.keys()):
            centers.append(np.mean(clusters[k], axis = 0))
        return centers
        
    old_centers = random.sample(X, k)
    centers = random.sample(X, k)

    while not equal(centers, old_centers):
        old_centers = centers        
        clusters = clusterize(X, centers)        
        centers = get_centers(clusters)

    return (centers, clusters)

def draw(centers, clusters, draw_clusters=False, kind = 'o', colors = "bgrcmykw"):
    color_index = 0

    def inc_color_index(color_index):
        if color_index == len(colors)-1:
            return 0
        return color_index + 1    

    for index, cluster in clusters.iteritems():
        if draw_clusters:
            x, y = [], []
            for a, b in cluster:
                x.append(a)
                y.append(b)
            plt.plot(x,y, kind+colors[color_index])

        if centers:            
            center = centers[index]
            plt.scatter([center[0]], [center[1]], s=500, color=colors[color_index])

        color_index = inc_color_index(color_index)
    #plt.show()


def init_board_gauss(N, k):
    n = float(N)/k
    X = []
    for i in range(k):
        c = (random.uniform(-1, 1), random.uniform(-1, 1))
        s = random.uniform(0.05,0.5)
        x = []
        while len(x) < n:
            a, b = np.array([np.random.normal(c[0], s), np.random.normal(c[1], s)])
            # Continue drawing points from the distribution in the range [-1,1]
            if abs(a) < 1 and abs(b) < 1:
                x.append([a,b])
        X.extend(x)
    X = np.array(X)[:N]
    return X

#X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(500)])

# X = init_board_gauss(1000, 3)
# centers, clusters = kmeans(X, 3)
# draw(centers, clusters)

import pandas
metro = pandas.read_csv('data_praga_metro_1.csv', sep=',')

stations = ['A0', 'A1', 'B0', 'B1', 'C0', 'C1']

#oil = [float(x) for x in list(oil['cost'])]
stations_dict = {}
total = []
for station in stations:
    a = [float(x) for x in list(metro['th'+station])]
    b = [float(x) for x in list(metro['r'+station])]
    stations_dict[station] = [np.array(x) for x in zip(a,b)]
    total.extend(stations_dict[station])

#print stations_dict

centers, clusters = kmeans(total, 6)

def find_station(point, stations_dict):
    x,y = point
    for station, data in stations_dict.iteritems():
        for point in data:
            x1, y1 = point
            if x==x1 and y==y1:
                return station


for index, cluster in clusters.iteritems():
    print 'cluster %d:' % index, 
    for point in cluster:
        print find_station(point, stations_dict),
    print ''

draw(centers, clusters, draw_clusters=True, kind='-', colors='c')
draw(None, stations_dict, draw_clusters=True, kind='o',  colors = "bgrmykw")

plt.xlabel(u'Среднее число пассажиров, вошедших с данной станции в метрополитена в день.')
plt.ylabel(u'Среднее число пассажиров, вышедших с данной станции в день.')
plt.show()
