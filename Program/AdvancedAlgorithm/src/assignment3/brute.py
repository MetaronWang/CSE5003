import json
import time
from pathlib import Path

import numpy as np
from multiprocessing import Process, Manager


def calculate(index, plans, all_task, return_dict):
    total_min, min_plan = 10000000000, -1
    for plan in plans:
        max_time, max_machine = -1, -1
        for m in range(len(plan)):
            time = sum([all_task[i][m] for i in plan[m]])
            if time > max_time:
                max_time, max_machine = time, m
        if max_time < total_min:
            total_min, min_plan = max_time, plan
    return_dict[index] = (total_min, min_plan)


def brute(path, all_plan):
    all_task = json.loads(open(Path(path, 'task.json'), 'r').read())
    process_num = 40
    all_plan = np.array_split(all_plan, process_num)
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    for i in range(process_num):
        p = Process(target=calculate, args=(i, all_plan[i], all_task, return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
    min_time, min_plan = 100000, []
    for i in return_dict.keys():
        if return_dict[i][0] < min_time:
            min_time, min_plan = return_dict[i]
    min_plan = [list(i)for i in min_plan]
    return min_time, min_plan