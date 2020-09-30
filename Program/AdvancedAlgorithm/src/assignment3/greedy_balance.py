import json
from pathlib import Path
from assignment2.pic import printPic


def greedy_balance(path):
    all_task = json.loads(open(Path(path, 'task.json'), 'r').read())
    job_num, machine_num = len(all_task), len(all_task[0])
    task_sum = [sum(i) for i in all_task]
    machine_time = [0 for i in range(machine_num)]
    machine_tasks = [[] for i in range(machine_num)]
    job_finished = []
    for i in range(job_num):
        min_index, min_time = -1, 100000000000
        target_job, target_cost = -1, -1
        for index in range(len(task_sum)):
            if task_sum[index] > target_cost and index not in job_finished:
                target_job, target_cost = index, task_sum[index]
        for m in range(machine_num):
            if machine_time[m]+all_task[target_job][m] < min_time:
                min_index, min_time = m, machine_time[m]+all_task[target_job][m]
        machine_time[min_index] += all_task[target_job][min_index]
        machine_tasks[min_index].append(target_job)
        job_finished.append(target_job)
    return max(machine_time), machine_tasks

if __name__ == '__main__':
    greedy_balance('./')
