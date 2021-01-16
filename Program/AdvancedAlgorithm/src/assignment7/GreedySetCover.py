import random
from itertools import combinations
from networkx.algorithms import bipartite
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

task_num = 10

machine_num = 6

machine_info = []

color = ['DeepPink', 'SpringGreen', 'Cyan', 'PaleVioletRed', 'GoldEnrod', 'OrangeRed', 'Tomato']


def greedy():
    r = {i for i in range(task_num)}
    m = {i for i in range(machine_num)}
    s = []
    while len(r) > 0:
        choice = min(m, key=lambda item: machine_info[item][1] / max(len(r & set(machine_info[item][0])) * 1.0, 0.001))
        s.append(choice)
        for i in machine_info[choice][0]:
            if i in r:
                r.remove(i)
        m.remove(choice)

    return s, sum([machine_info[i][1] for i in s])


def brute():
    min_value, min_team = 10000000000, []
    for i in range(machine_num):
        xx = list(combinations(range(machine_num), i + 1))
        for m in xx:
            task_count = [0 for i in range(task_num)]
            for index in m:
                for t in machine_info[index][0]:
                    task_count[t] += 1
            if 0 not in task_count:
                cost = sum([machine_info[index][1] for index in m])
                if cost < min_value:
                    min_value, min_team = cost, m
    return min_team, min_value


def generate_date():
    global machine_info
    task_count = [0 for i in range(task_num)]
    while 0 in task_count or 1 in task_count:
        machine_info = [[] for i in range(machine_num)]
        task_count = [0 for i in range(task_num)]
        temp = [i for i in range(machine_num)]
        random.shuffle(temp)
        for i in temp:
            machine_info[i].append([])
            while len(machine_info[i][0]) == 0:
                for j in range(task_num):
                    if random.random() * ((machine_num - task_count[j]) / machine_num) > 0.5:
                        machine_info[i][0].append(j)
                        task_count[j] += 1
                    if len(machine_info[i][0]) > 3*task_num//5:
                        break
            machine_info[i].append(random.random() * 3 * len(machine_info[i][0]) + len(machine_info[i][0]))


def draw_pic():
    plt.clf()
    plt.axis('off')
    B = nx.Graph()
    # Add nodes with the node attribute "bipartite"
    # B.add_nodes_from(["M{}".format(i) for i in range(machine_num)], bipartite=0, color='red')
    for i in range(machine_num):
        B.add_node("M{}".format(i), bipartite=0, color=color[i])
    B.add_nodes_from(["T{}".format(i) for i in range(task_num)], bipartite=1)
    # Add edges only between nodes of opposite node sets
    edge_color = []
    for i in range(machine_num):
        B.add_edges_from([("M{}".format(i), "T{}".format(j)) for j in machine_info[i][0]])
        edge_color += [color[i] for j in machine_info[i][0]]
    # nx.draw(B)
    X, Y = bipartite.sets(B)
    length = max(len(X) - 1, len(Y) - 1)
    pos = dict()
    pos.update((n, (i * length / (len(X) - 1), 2)) for i, n in [(i, "M{}".format(i)) for i in range(machine_num)])
    pos.update((n, (i * length / (len(Y) - 1), 1)) for i, n in [(i, "T{}".format(i)) for i in range(task_num)])
    nx.draw_networkx(B, pos=pos, node_size=800, edge_color=edge_color,
                     nodelist=["M{}".format(i) for i in range(machine_num)] + ["T{}".format(i) for i in
                                                                               range(task_num)],
                     node_color=[color[i] for i in range(machine_num)] + ['LightSkyBlue' for i in range(task_num)])
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0.1, 0.1)
    plt.savefig('./result/1.svg', dpi=1000)
    plt.show()


if __name__ == '__main__':
    random.seed(132423132000)
    generate_date()
    t1, v1 = greedy()
    t2, v2 = brute()
    last = 1
    while v1 / v2 < 2:
        print("\r{}".format(max(last, v1 / v2)), end='')
        generate_date()
        t1, v1 = greedy()
        t2, v2 = brute()
        last = max(last, v1 / v2)
    print("\r{}".format(max(last, v1 / v2)), end='')
    print()
    print(machine_info)
    print(t1, v1)
    print(t2, v2)
    draw_pic()
    exit()
