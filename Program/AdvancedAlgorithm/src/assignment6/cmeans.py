import copy
import json
import math

import numpy as np
from typing import List

import os

from assignment6.pic import *
import random
from multiprocessing import Process, Manager


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


class CMeans:
    def __init__(self, points, k, m=3):
        self.k = k
        self.points = points
        self.centers = [[0, 0] for i in range(self.k)]
        self.u = [[random.random() for i in range(self.k)] for p in points]
        self.m = m

    def update_center(self):
        for j in range(self.k):
            self.centers[j] = (
                sum([self.points[i][0] * (self.u[i][j] ** self.m) for i in range(len(self.points))]) / sum(
                    [self.u[i][j] ** self.m for i in range(len(self.points))]),
                sum([self.points[i][1] * (self.u[i][j] ** self.m) for i in range(len(self.points))]) / sum(
                    [self.u[i][j] ** self.m for i in range(len(self.points))])
            )

    def update_u(self):
        for i in range(len(self.points)):
            for j in range(self.k):
                self.u[i][j] = sum([(dist(self.points[i], self.centers[j]) / dist(self.points[i],
                                                                                  self.centers[k])) ** (
                                            2.0 / (self.m - 1)) for k in range(self.k)]) ** -1

    def eval_dis(self):
        distance = 0
        for j in range(self.k):
            distance += sum([dist(self.points[i], self.centers[j]) * (self.u[i][j] ** self.m) for i in
                             range(len(self.points))])
        return distance


class KMeans:
    def __init__(self, points, k):
        self.k = k
        self.points = points
        self.centers = []
        self.clusters = [[] for i in range(self.k)]

    def update_center(self):
        for index in range(len(self.clusters)):
            cluster = self.clusters[index]
            if len(cluster) > 0:
                self.centers[index] = (
                    sum([p[0] for p in cluster]) / len(cluster), sum([p[1] for p in cluster]) / len(cluster))

    def update_cluster(self):
        self.clusters = [[] for i in range(self.k)]
        c = range(self.k)
        for p in self.points:
            self.clusters[min(c, key=lambda item: (self.centers[item][0] - p[0]) ** 2 + (
                    self.centers[item][1] - p[1]) ** 2)].append(p)

    def eval_dis(self):
        distance = 0
        for i in range(self.k):
            distance += sum(
                [(self.centers[i][0] - p[0]) ** 2 + (self.centers[i][1] - p[1]) ** 2 for p in self.clusters[i]])
        return distance


class InitialCenterSelect:
    """
    Use for choice the initial center site for kmeans
    """

    def __init__(self, points_map: List[List[int]], k: int):
        self.map = points_map
        self.k = k
        matrix = [[0 for i in range(len(self.map))] for j in range(len(self.map))]
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                matrix[i][j] = ((self.map[i][0] - self.map[j][0]) ** 2 + (self.map[i][1] - self.map[j][1]) ** 2) ** 0.5
        self.adjacency_matrix = matrix

    def get_first_center(self):
        size = len(self.adjacency_matrix)
        s = range(size)
        start = min(s, key=lambda item: max(sorted(self.adjacency_matrix[item])[:size // 3 + 1]))
        return start

    def center_select(self):
        s = [i for i in range(len(self.map))]
        start = self.get_first_center()
        c = [start]
        del s[start]
        for i in range(self.k - 1):
            index = max(s, key=lambda item: min([self.adjacency_matrix[center][item] for center in c]))
            del s[s.index(index)]
            c.append(index)
        return c, [self.map[i] for i in c]


def gen_map(num, k, region):
    random.seed(1000)
    centers = []
    points = []
    while len(centers) < k:
        valid = False
        time = 0
        while not valid:
            time += 1
            x = random.random() * region // 2 + region // 4
            y = random.random() * region // 2 + region // 4
            valid = True
            for p in centers:
                d = pow(pow(x - p[0], 2) + pow(y - p[1], 2), 0.5)
                if d < region // k:
                    valid = False
                    break
            if valid:
                centers.append([x, y])
            elif time > 1000:
                centers = []
    while len(points) < num:
        x = random.random() * region
        y = random.random() * region
        p = max([1.5 ** -(dist(center, (x, y))) for center in centers])
        # if p > random.random():
        points.append([x, y])
    print('init')
    return points


def make_example(region, size, k, m, gif=False):
    cmeans = CMeans(gen_map(size, k, region), k, m)
    cmeans.update_center()
    init = 'u_{}'.format(m)
    if not os.path.exists('result/{}'.format(init)):
        os.mkdir('result/{}'.format(init))
    last_value = copy.deepcopy(cmeans.centers)
    all_num = 0
    process_list = []
    for i in range(200):
        cmeans.update_u()
        # print(i, cmeans.eval_dis())
        if gif:
            p = Process(target=print_pic,
                        args=(
                            cmeans.points, cmeans.centers, cmeans.u, m, region,
                            '{}/cmeans_{}'.format(init, 2 * i),))
            process_list.append(p)
            p.start()
        cmeans.update_center()
        # print(i, cmeans.eval_dis())
        if gif:
            p = Process(target=print_pic,
                        args=(cmeans.points, cmeans.centers, cmeans.u, m, region,
                              '{}/cmeans_{}'.format(init, 2 * i + 1),))
            process_list.append(p)
            p.start()
        diff = max([dist(last_value[j], cmeans.centers[j]) for j in range(k)])
        all_num = 2 * i
        if diff < 10e-15:
            print(i)
            break
        else:
            print(diff)
        last_value = copy.deepcopy(cmeans.centers)
    print_pic(cmeans.points, cmeans.centers, cmeans.u, m, region, 'cmeans_{}'.format(m), dpi=1000)
    for p in process_list:
        p.join()
    if gif:
        Process(target=create_gif, args=(init, all_num)).start()


def make_kmeans_example(region, size, k, gif=False):
    kmeans = KMeans(gen_map(size, k, region), k)
    _, kmeans.centers = InitialCenterSelect(kmeans.points, kmeans.k).center_select()
    kmeans.update_center()
    init = 'center'
    if not os.path.exists('result/{}'.format(init)):
        os.mkdir('result/{}'.format(init))
    last_value = copy.deepcopy(kmeans.centers)
    all_num = 0
    process_list = []
    for i in range(20):
        kmeans.update_cluster()
        if gif:
            p = Process(target=print_kmeans_pic,
                        args=(
                            kmeans.points, kmeans.centers, kmeans.clusters, region,
                            '{}/kmeans_{}'.format(init, 2 * i),))
            process_list.append(p)
            p.start()
        kmeans.update_center()
        if gif:
            p = Process(target=print_kmeans_pic,
                        args=(kmeans.points, kmeans.centers, kmeans.clusters, region,
                              '{}/kmeans_{}'.format(init, 2 * i + 1),))
            process_list.append(p)
            p.start()
        diff = max([dist(last_value[j], kmeans.centers[j]) for j in range(k)])
        all_num = 2 * i
        if diff < 10-15:
            print(i)
            break
        # else:
        #     print(diff)
        last_value = copy.deepcopy(kmeans.centers)
    if not gif:
        print_kmeans_pic(kmeans.points, kmeans.centers, kmeans.clusters, region, 'kmeans', dpi=1000)
    for p in process_list:
        p.join()
    if gif:
        Process(target=create_gif, args=(init, all_num, 'kmeans')).start()


if __name__ == '__main__':
    # statistic()
    # make_example(20, 3000, 5, 1.1)
    # make_example(20, 3000, 5, 1.5)
    make_example(5, 100000, 5, 2)
    # make_example(20, 3000, 5, 3)
    # make_kmeans_example(20, 3000, 3, gif=True)
    # make_example(20, 7000, 7, 2, gif=True)
