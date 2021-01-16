import json
import os
import time
from pathlib import Path
import numpy as np
from assignment3.brute import *
from assignment3.generateTask import generateTask, generatePlan
from assignment3.greedy_balance import greedy_balance
from assignment3.pic import printPic
from assignment3.statistic import statistic
from tqdm import tqdm


def get_resut(job_num, machine_num, test_num):
    print("Job NUM: {}; Machine NUM: {}".format(job_num, machine_num))
    root_dir = "result_{}_{}".format(job_num, machine_num)
    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)
    if os.path.exists(Path(root_dir, 'plan.npy')):
        all_plan = np.load(Path(root_dir, 'plan.npy'), allow_pickle=True)
    else:
        all_plan = generatePlan(root_dir, job_num, machine_num)
    print(len(all_plan))
    all_value = []
    for index in tqdm(range(test_num)):
        # print("\r{}/{}".format(index, test_num), end="")
        path = "{}/sample_{}/".format(root_dir, index)
        if not os.path.isdir(path):
            os.mkdir(path)
        task = generateTask(path, job_num, machine_num)
        min_time, min_plan = brute(path, all_plan)
        greedy_time, greedy_plan = greedy_balance(path)
        value = {'min_time': min_time, 'min_plan': min_plan, 'greedy_time': greedy_time, 'greedy_plan': greedy_plan,
                 'quality': greedy_time / min_time, 'task': task}
        open(Path(path, 'value.json'), 'w').write(json.dumps(value))
        all_value.append(value)
        printPic(greedy_plan, task, path, 'greedy_balance')
        printPic(min_plan, task, path, 'optimal')
    open(Path(root_dir, 'all_value.json'), 'w').write(json.dumps(all_value))
    statistic(job_num, machine_num)


if __name__ == '__main__':
    # get_resut(11, 5, 1000)
    # get_resut(9, 4, 1000)
    # get_resut(7, 3, 1000)
    statistic(11, 5)
    statistic(9, 4)
    statistic(8, 3)
    statistic(7, 3)
