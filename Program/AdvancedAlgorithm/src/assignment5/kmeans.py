import json

import numpy as np
from typing import List
from assignment5.pic import print_pic
import random
from multiprocessing import Process, Manager


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


class InitialClusterSelect:
    """
    Use for choice the initial site cluster for kmeans
    """

    def __init__(self, points_map: List[List[int]], k: int):
        self.map = points_map
        self.k = k
        initialCenter = InitialCenterSelect(points_map, k)
        self.choice, _ = initialCenter.center_select()
        self.adjacency_matrix = initialCenter.adjacency_matrix
        self.clusters = [[i] for i in self.choice]
        self.point_rest = set(range(len(points_map))) - set(self.choice)

    def cluster_select(self):
        while len(self.point_rest) > 0:
            for c_index in range(self.k):
                index = min(self.point_rest,
                            key=lambda item: min([self.adjacency_matrix[item][ci] for ci in self.clusters[c_index]]))
                self.clusters[c_index].append(index)
                self.point_rest.remove(index)
                if len(self.point_rest) <= 0:
                    break
        return [[self.map[i] for i in c] for c in self.clusters]


def gen_map(num, region):
    # random.seed(1000)
    map = []
    while len(map) < num:
        site = [random.randint(1, region), random.randint(1, region)]
        if site not in map:
            map.append(site)
    return map


def make_example():
    region = 80
    size = 2000
    k = 100
    kmeans = KMeans(gen_map(size, region), k)
    # kmeans.centers = [kmeans.points[i] for i in range(k)]
    # kmeans.clusters = [[kmeans.points[i]] for i in range(k-1)]
    # kmeans.clusters.append([i for i in kmeans.points[k:]])
    _, kmeans.centers = InitialCenterSelect(kmeans.points, kmeans.k).center_select()
    kmeans.update_cluster()
    init = 'center'
    # kmeans.clusters = InitialClusterSelect(kmeans.points, kmeans.k).cluster_select()
    # kmeans.centers = [(0, 0) for i in range(k)]
    # init = 'cluster'
    for i in range(20):
        kmeans.update_center()
        print(i, kmeans.eval_dis())
        Process(target=print_pic,
                args=(
                kmeans.points, kmeans.centers, kmeans.clusters, region, '{}/kmeans_{}'.format(init, 2 * i),)).start()
        kmeans.update_cluster()
        print(i, kmeans.eval_dis())
        Process(target=print_pic,
                args=(kmeans.points, kmeans.centers, kmeans.clusters, region,
                      '{}/kmeans_{}'.format(init, 2 * i + 1),)).start()
    print_pic(kmeans.points, kmeans.centers, kmeans.clusters, region, 'kmeans_1')


def get_data(index, num, region, size, k, return_dict):
    data = []
    for i in range(num):
        test_map = gen_map(size, region)
        kmeans = KMeans(test_map, k)
        _, kmeans.centers = InitialCenterSelect(kmeans.points, kmeans.k).center_select()
        kmeans.update_cluster()
        last_value = 100000000000
        for i in range(80):
            kmeans.update_center()
            test_value = kmeans.eval_dis()
            if test_value >= last_value:
                break
            last_value = test_value
            kmeans.update_cluster()
            test_value = kmeans.eval_dis()
            if test_value >= last_value:
                break
            last_value = test_value
        center_value = kmeans.eval_dis()
        kmeans = KMeans(test_map, k)
        kmeans.clusters = InitialClusterSelect(kmeans.points, kmeans.k).cluster_select()
        kmeans.centers = [(0, 0) for i in range(k)]
        last_value = 100000000000
        for i in range(80):
            kmeans.update_center()
            test_value = kmeans.eval_dis()
            if test_value >= last_value:
                break
            last_value = test_value
            kmeans.update_cluster()
            test_value = kmeans.eval_dis()
            if test_value >= last_value:
                break
            last_value = test_value
        cluster_value = kmeans.eval_dis()
        data.append([center_value, cluster_value])
    return_dict[index] = data


if __name__ == '__main__':
    case_num = 125
    process_num = 40
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    for i in range(process_num):
        p = Process(target=get_data, args=(i, case_num, 80, 2000, 100, return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
    all_data = []
    for i in range(process_num):
        all_data += return_dict[i]
    open('statistic.json','w').write(json.dumps(all_data))