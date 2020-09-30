import json
import os
from pathlib import Path
import numpy as np
from assignment2.brute import brute
from assignment2.generateTask import generateTask
from multiprocessing import Process
from multiprocessing import Manager

from assignment2.greedy_balance import greedy_balance
from assignment2.pic import printPic


def get_resut(i, task_num, machine_num, return_dict):
    path = "{}/sample_{}/".format(root_dir, i)
    if not os.path.isdir(path):
        os.mkdir(path)
    task = generateTask(path, machine_num)
    # min_time, min_plan = brute(path, machine_num)
    greedy_time, greedy_plan = greedy_balance(path, machine_num)
    # value = [min_time, min_plan, greedy_time, greedy_plan, sum(task) / machine_num, task]
    # open(Path(path, 'value.json'), 'w').write(json.dumps(value))
    # return_dict[i] = value
    printPic(greedy_plan, task, path, 'greedy_balance')
    # printPic(min_plan, task, path, 'optimal')


if __name__ == '__main__':
    task_num = 17
    machine_num = 8
    experiment_num = 1
    core_num = 40
    root_dir = "result_{}_{}".format(task_num, machine_num)
    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)
    manager = Manager()
    return_dict = manager.dict()
    process_list = []
    result = []
    for i in range(experiment_num):
        if i % 100 == 0:
            print("\r{}".format(i), end='')
        p = Process(target=get_resut, args=(i % core_num, task_num, machine_num, return_dict))  # 实例化进程对象
        p.start()
        process_list.append(p)
        if len(process_list) >= core_num:
            for p in process_list:
                p.join()
            process_list.clear()
    for p in process_list:
        p.join()
    # for i in range(experiment_num):
    #     result.append(return_dict[i])
    # open(Path(root_dir, 'result.json'), 'w').write(json.dumps(result))
