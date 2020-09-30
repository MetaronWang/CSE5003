import json
import time

import numpy as np
from multiprocessing import Process
from multiprocessing import Manager


def fun1(index, paths, distance_matrix, return_dict):
    min = 10000000000
    min_path = []
    for path in paths:
        distance = sum([distance_matrix[path[i - 1]][path[i]] for i in range(1,len(path))])
        if distance < min:
            min = distance
            min_path = path
    return_dict[index] = [min, min_path]


def brute(path):
    distance_matrix =  np.load(path+'distance.npy')
    start = time.time()
    process_num = 40
    paths = np.load('path.npy')
    paths = np.array_split(paths, process_num)
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    for i in range(process_num):
        p = Process(target=fun1, args=(i, paths[i], distance_matrix, return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    min = 10000000000
    min_path = []
    for i in return_dict:
        if return_dict[i][0] < min:
            min = return_dict[i][0]
            min_path =return_dict[i][1]
    print(time.time() - start)
    # print(min, list(min_path))
    return(min, list(min_path))


if __name__ == '__main__':
    print(brute('./'))