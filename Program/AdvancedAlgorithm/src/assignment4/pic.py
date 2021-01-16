import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from assignment4.center_select import center_select, get_max_dis, brute_select
from assignment4.gen_map import gen_map
from tqdm import tqdm


def statistic():
    plt.clf()
    data = json.loads(open('result/qualities.json','r').read())
    greedy_quality = [i[0] for i in data]
    optimal_quality = [i[1] for i in data]
    plt.hist(x=greedy_quality, bins=80, color='MediumSpringGreen', alpha=0.7, rwidth=0.8)
    plt.xlabel('Greedy Quality Range')
    plt.ylabel('Number')
    plt.savefig('result/greedy_quality.jpg',dpi=1000)
    plt.clf()
    plt.hist(x=optimal_quality, bins=80, color='MediumSpringGreen', alpha=0.7, rwidth=0.8)
    plt.xlabel('Optimal Greedy Quality Range')
    plt.ylabel('Number')
    plt.savefig('result/optimal_quality.jpg',dpi=1000)




def print_pic(map, c, center_sites, region, name):
    plt.clf()
    plt.grid()
    plt.axis([1, region+1, 1, region+1])
    plt.xticks(range(0, region + 1))
    plt.yticks(range(0, region + 1))
    for center in c:
        for site in center_sites[center]:
            plt.plot([map[center][0], map[site][0]], [map[center][1], map[site][1]], color='g')
    plt.scatter([i[0] for i in map], [i[1] for i in map],zorder=30)
    plt.scatter([map[i][0] for i in c], [map[i][1] for i in c], color='r', s=80,zorder=50)
    plt.savefig('result/{}.jpg'.format(name),dpi=1000)


if __name__ == '__main__':
    region = 10
    center_num = 5
    qualities = []
    statistic()
    # for i in tqdm(range(1000)):
    #     map = gen_map(40, region)
    #     # map = [[3,2], [3,3], [3,4], [2,3], [4,3], [3,5], [3,6]]
    #     # print('--------brute-----------')
    #     c, adjacency_matrix = brute_select(map, center_num)
    #     max_dis, center_sites = get_max_dis(map, adjacency_matrix, c)
    #     # print(max_dis)
    #     # print(c)
    #     brute_dis = max_dis
    #     print_pic(map, c, center_sites, region, 'brute')
    #     # print('--------greedy-----------')
    #     c, adjacency_matrix = center_select(map, center_num)
    #     max_dis, center_sites = get_max_dis(map, adjacency_matrix, c)
    #     # print(max_dis)
    #     # print(c)
    #     # print('Quality is {}'.format(max_dis/brute_dis))
    #     # print_pic(map, c, center_sites, region, 'greedy')
    #     greedy_qualty = max_dis/brute_dis
    #     max_c = c
    #     for i in range(len(map)):
    #         c, adjacency_matrix = center_select(map, center_num, i)
    #         max_dis_tmp, center_sites_tmp = get_max_dis(map, adjacency_matrix, c)
    #         if max_dis_tmp < max_dis:
    #             max_dis, center_sites, max_c = max_dis_tmp, center_sites_tmp, c
    #     # print(max_dis)
    #     # print(max_c)
    #     # print('Best Quality is {}'.format(max_dis / brute_dis))
    #     # print_pic(map, max_c, center_sites, region, 'greedy_optimal')
    #     optimal_qualty = max_dis / brute_dis
    #     qualities.append([greedy_qualty, optimal_qualty])
    #     open('result/qualities','w').write(json.dumps(qualities))

