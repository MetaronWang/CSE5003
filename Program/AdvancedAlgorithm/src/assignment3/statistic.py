from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np


def statistic(job_num, machine_num):
    plt.clf()
    all_value = json.loads(open(Path('result_{}_{}'.format(job_num, machine_num), 'all_value.json'), 'r').read())
    qualities = np.array([i['quality'] for i in all_value])
    hist, bin_edge = np.histogram(qualities, bins=30)
    print(hist, bin_edge)
    n,bins,patches = plt.hist(x=qualities, bins=30,color='MediumSpringGreen', alpha=0.7, rwidth=0.8)
    plt.xlabel('Quality Range')
    plt.ylabel('Number')
    plt.title('Job num is {}, Machine num is {}'.format(job_num, machine_num))
    plt.text(bins[len(bins)//2], max(hist)*0.8,
             'We test {} cases\nthe average quality is {:.4}'.format(len(qualities), np.average(qualities))
             )
    plt.savefig('statistic/result_{}_{}.jpg'.format(job_num, machine_num), dpi=500)
    plt.savefig('statistic/result_{}_{}.jpg'.format(job_num, machine_num), dpi=500)

if __name__ == '__main__':
    statistic(8, 3)