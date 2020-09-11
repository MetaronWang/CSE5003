import json
import time

import numpy as np
from multiprocessing import Process
from multiprocessing import Manager

from assignment1.pic import printPic


def fun1(start, distance_matrix, return_dict):
    distance = 0
    path = [start]
    current_city = start
    arrived_city = set()
    arrived_city.add(current_city)

    while len(path) < 10:
        min = 100000000
        min_city = current_city
        for i in range(10):
            if current_city != i and i not in arrived_city:
                if distance_matrix[current_city][i] < min:
                    min = distance_matrix[current_city][i]
                    min_city = i
        distance += distance_matrix[current_city][min_city]
        current_city = min_city
        path.append(current_city)
        arrived_city.add(current_city)
    distance += distance_matrix[current_city][start]
    path.append(start)
    return_dict[start] = [distance, path]


def NNG(path):
    distance_matrix = np.load(path + 'distance.npy')
    start = time.time()
    process_num = 10
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    for i in range(process_num):
        p = Process(target=fun1, args=(i, distance_matrix, return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    min = 10000000000
    min_path = []
    for i in return_dict:
        if return_dict[i][0] < min:
            min = return_dict[i][0]
            min_path = return_dict[i][1]
    print(time.time() - start)
    # print(min, min_path)
    return (min, min_path)
if __name__ == '__main__':
    min, min_path = NNG('./')
    printPic(min_path, min)