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

def draw(centers, clusters):
    colors = "bgrcmykw"
    color_index = 0

    for index, cluster in clusters.iteritems():
        x, y = [], []
        for a, b in cluster:
            x.append(a)
            y.append(b)

        plt.plot(x,y, 'o'+colors[color_index])
        center = centers[index]
        plt.scatter([center[0]], [center[1]], s=500, color=colors[color_index])
        color_index += 1
    plt.show()


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

X = init_board_gauss(1000, 3)
centers, clusters = kmeans(X, 3)
draw(centers, clusters)