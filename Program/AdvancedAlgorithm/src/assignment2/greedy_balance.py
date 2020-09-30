import json
from pathlib import Path
from assignment2.pic import printPic


def greedy_balance(path, machine_num):
    all_task = json.loads(open(Path(path, 'task.json'), 'r').read())
    machines_rest_time = [0 for i in range(machine_num)]
    total_time = 0
    task_finish = []
    task_machine = [[] for i in range(machine_num)]
    while len(all_task) > len(task_finish):
        min_machine, min_time = 0, 100000000
        for i in range(machine_num):
            if machines_rest_time[i] < min_time:
                min_machine, min_time = i, machines_rest_time[i]
        for i in range(machine_num):
            machines_rest_time[i] -= min_time
            if machines_rest_time[i] == 0:
                max_value, max_index = 0, 0
                for j in range(len(all_task)):
                    if j not in task_finish and all_task[j] > max_value:
                        max_value, max_index = all_task[j], j
                machines_rest_time[i] += max_value
                task_finish.append(max_index)
                task_machine[i].append(max_index)
            if len(all_task) <= len(task_finish):
                break
        total_time += min_time
    total_time += max(machines_rest_time)
    return total_time, task_machine


def greedy_balance_by_order(path, machine_num):
    all_task = json.loads(open(Path(path, 'task.json'), 'r').read())
    machines_rest_time = [0 for i in range(machine_num)]
    total_time = 0
    task_machine = [[] for i in range(machine_num)]
    index = 0
    while index <= len(all_task):
        min_machine, min_time = 0, 100000000
        for i in range(machine_num):
            if machines_rest_time[i] < min_time:
                min_machine, min_time = i, machines_rest_time[i]
        for i in range(machine_num):
            machines_rest_time[i] -= min_time
            if machines_rest_time[i] == 0:
                machines_rest_time[i] += all_task[index]
                index += 1
                task_machine[i].append(index)
        total_time += min_time
    total_time += max(machines_rest_time)
    return total_time, task_machine


if __name__ == '__main__':
    greedy_balance('result_10_3/sample_0', 3)
