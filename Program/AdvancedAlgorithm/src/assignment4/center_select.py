import numpy as np
import json
from itertools import combinations
from typing import List
from tqdm import tqdm
from multiprocessing import Process, Manager

INF = 10000000000000000


def get_adjacency_matrix(map):
    matrix = [[0 for i in range(len(map))] for j in range(len(map))]
    for i in range(len(map)):
        for j in range(len(map)):
            matrix[i][j] = ((map[i][0] - map[j][0]) ** 2 + (map[i][1] - map[j][1]) ** 2) ** 0.5
    return matrix


def get_first_center(adjacency_matrix: List[List[float]]):
    size = len(adjacency_matrix)
    s = range(size)
    start = min(s, key=lambda item: max(sorted(adjacency_matrix[item])[:size//3+1]))
    return start

def center_select(map: List[List[int]], k: int, start=-1):
    s = [i for i in range(len(map))]
    adjacency_matrix = get_adjacency_matrix(map)
    if start < 0:
        start = get_first_center(adjacency_matrix)
    c = [start]
    del s[start]
    for i in range(k - 1):
        index = max(s, key=lambda item: min([adjacency_matrix[center][item] for center in c]))
        del s[s.index(index)]
        c.append(index)
    return c, adjacency_matrix


def calculate(index, cal_c, map, adjacency_matrix, return_dict):
    min_c, min_value = [], INF
    for c in cal_c:
        max_dis, _ = get_max_dis(map, adjacency_matrix, c)
        if max_dis < min_value:
            min_c, min_value = c, max_dis
    return_dict[index] = [min_c, min_value]


def brute_select(map: List[List[int]], k: int):
    adjacency_matrix = get_adjacency_matrix(map)
    all_c = list(combinations(range(len(map)), k))
    process_num = 40
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    all_c = np.array_split(all_c, process_num)
    for i in range(process_num):
        p = Process(target=calculate, args=(i, all_c[i], map, adjacency_matrix, return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)
    min_c, min_value = [], INF
    for p in process_list:
        p.join()
    for i in range(process_num):
        if return_dict[i][1] < min_value:
            min_c, min_value = return_dict[i][0], return_dict[i][1]
    return min_c, adjacency_matrix


def get_max_dis(map, adjacency_matrix, c):
    max_dis = 0
    center_sites = [[] for i in range(len(map))]
    for i in range(len(map)):
        center = min(c, key=lambda item: [adjacency_matrix[i][item]])
        dis = adjacency_matrix[i][center]
        center_sites[center].append(i)
        if dis > max_dis:
            max_dis = dis
    return max_dis, center_sites
