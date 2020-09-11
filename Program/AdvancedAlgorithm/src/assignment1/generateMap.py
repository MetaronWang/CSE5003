import itertools
import json
import random
import numpy as np


def getAllPaths(n):
    all = list(itertools.permutations(range(n), n))
    for i in range(len(all)):
        all[i] = all[i] + (all[i][0],)
    print(np.array(all).shape)
    np.save("path.npy", np.array(all))


def getPoints(n, path='./'):
    points = []
    while len(points) < n:
        valid = False
        time = 0
        while not valid:
            time += 1
            x = random.random() * 100
            y = random.random() * 100
            valid = True
            for p in points:
                d = pow(x - p[0], 2) + pow(y - p[1], 2)
                if d < 1200:
                    valid = False
                    break
            if valid:
                points.append([x, y])
            elif time>1000:
                points = []

    open(path + 'points.json', 'w').write(json.dumps(points))


def getDistance(n, path='./'):
    distance_matrix = np.zeros([n, n])
    citys = json.loads(open(path + 'points.json', 'r').read())
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = pow(pow(citys[i][0] - citys[j][0], 2) + pow(citys[i][1] - citys[j][1], 2), 0.5)
    np.save(path + 'distance.npy', distance_matrix)


if __name__ == '__main__':
    getPoints(10)
    getDistance(10)
    getAllPaths(10)
