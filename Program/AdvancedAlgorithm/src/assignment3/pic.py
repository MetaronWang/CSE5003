from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def printPic(task_machine, all_task, path, type):
    plt.clf()
    max_num = max([len(i) for i in task_machine])
    bar_data = [[all_task[task_machine[j][i]][j] if len(task_machine[j]) > i else 0 for j in range(len(task_machine))] for i in range(max_num)]
    bar_start = [np.sum(bar_data[:i], axis=0) for i in range(len(bar_data))]
    labels = ['Machine{}'.format(i) for i in range(len(task_machine))]
    plt.barh(labels, bar_data[0])
    for i in range(1, len(bar_data)):
        plt.barh(labels, bar_data[i], left=bar_start[i])
    for i in range(len(task_machine)):
        for j in range(len(task_machine[i])):
            plt.text(bar_start[j][i] + bar_data[j][i] / 2 if j > 0 else bar_data[j][i] / 2, i,
                     'J{}'.format(task_machine[i][j]))
    plt.savefig(Path(path, '{}.jpg'.format(type)), dpi=1000)
    # plt.show()


if __name__ == '__main__':
    m = 9
    task_machine = [[] for i in range(m)]
    all_task = [m for i in range(m-1)] + [1 for i in range(m)]+[m]
    for i in range(m-1):
        task_machine[i].append(i)
    for i in range(m):
        task_machine[m-1].append(i+m-1)
    task_machine[0].append(2*m-1)

    # all_task = []
    # for i in range(m):
    #     all_task.append(m)
    #     all_task.append(1)
    # for i in range(m):
    #     task_machine[i].append(2*i)
    #     task_machine[i].append(2*i+1)

    printPic(task_machine, all_task, './', 'greedy')
