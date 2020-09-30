import json
import random
from multiprocessing import Manager
from multiprocessing import Process, Value, Lock, Pool, Manager
import numpy as np
import sys
import copy
import itertools
from itertools import product

from pathlib import Path


def generateTask(path, job_num, machine_num, upper=10, lower=1):
    task = []
    for i in range(job_num):
        base = random.randint(lower, upper)
        task.append([base * (random.random() + 0.5) for i in range(machine_num)])
    open(Path(path, 'task.json'), 'w').write(json.dumps(task))
    return task


def recursion_stirling_set(n, k):
    if k == 1:
        return [[[x for x in range(n)]]]
    elif n == k:
        return [[[x] for x in range(n)]]
    else:
        temp_n = n
        temp_k = k
        s_n_1_k_1 = recursion_stirling_set(temp_n - 1, temp_k - 1)
        for i in range(len(s_n_1_k_1)):
            s_n_1_k_1[i].append([temp_n - 1])

        k_s_n_1_k = []
        temp = recursion_stirling_set(temp_n - 1, temp_k)
        for i in range(k):
            temp_ = copy.deepcopy(temp)
            k_s_n_1_k += temp_
        for i in range(len(temp) * k):
            k_s_n_1_k[i][int(i / len(temp))] += [temp_n - 1]

        return (s_n_1_k_1 + k_s_n_1_k)


def generatePlan(path, job_num, machine_num):
    solution = recursion_stirling_set(job_num, machine_num)
    solution_permutation = []
    for i in solution:
        solution_permutation += list(itertools.permutations(i, len(i)))
    solution = np.array(solution_permutation, dtype=object)
    np.save(Path(path,'plan.npy'), solution)
    return solution


if __name__ == '__main__':
    generatePlan('./', 8, 4)
