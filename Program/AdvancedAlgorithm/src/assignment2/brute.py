import json
from pathlib import Path

import numpy as np
from multiprocessing import Process, Value, Lock, Pool, Manager
from time import sleep

all_task = []

min_time = 1000000000

min_plan = []


def calculate(plan, machine_num):
    global all_task, min_plan, min_time
    plan = np.array(plan)
    all_time = 0
    for i in range(machine_num):
        idx = np.where(plan == i)[0]
        time = sum([all_task[index] for index in idx])
        all_time = time if time > all_time else all_time
    if all_time > 0 and min_time > all_time:
        min_time = all_time
        min_plan = plan


def elementFlag(elements, max_len, machine_num):
    global min_time
    if len(elements) >= max_len:
        calculate(elements, machine_num)
    else:
        for i in range(machine_num):
            elementFlag(elements + [i], max_len, machine_num)


def brute(path, machine_num):
    global all_task, min_plan, min_time
    all_task = json.loads(open(Path(path, 'task.json'), 'r').read())
    elementFlag([], len(all_task), machine_num)
    task_machine = [[] for i in range(machine_num)]
    for i in range(len(min_plan)):
        task_machine[min_plan[i]].append(i)
    return min_time, task_machine
