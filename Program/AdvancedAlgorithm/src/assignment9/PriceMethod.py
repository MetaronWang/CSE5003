import copy
import random
from itertools import permutations
from multiprocessing import Process, Manager
from assignment9.BuildMap import VertexCover
import numpy as np


def calc(index, ees, v, return_dict):
    min_value, min_team = 10000000000, []
    for es in ees:
        cost = 0
        v.reset_color_and_edge()
        for e in es:
            v.edges[e].add_value(v.edges[e].can_add())
            if v.no_update():
                break
        for node in v.nodes:
            if node.is_tight():
                node.color = 'OrangeRed'
                cost += node.cost
        if cost < min_value:
            min_value, min_team = cost, es
    return_dict[index] = [min_value, min_team]



def price(node_num, figure_size, v=None, draw=False):
    if not v:
        v = VertexCover(node_num)
    cost = 0
    while not v.no_update():
        e = min(v.edges, key=lambda edge: edge.can_add() if edge.can_add() > 0 else 100000000)
        e.add_value(e.can_add())
    for node in v.nodes:
        if node.is_tight():
            node.color = 'OrangeRed'
            cost += node.cost
    if draw:
        v.print_map(draw_edge=True, figure_size=figure_size, name=1)
    return cost



def price_parallel(node_num, figure_size, v=None, draw=False):
    if not v:
        v = VertexCover(node_num)
    ees = list(permutations(range(len(v.edges)), len(v.edges)))
    print(len(ees))
    process_num = 40
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    all_ees = np.array_split(ees, process_num)
    for i in range(process_num):
        p = Process(target=calc, args=(i, all_ees[i], copy.copy(v), return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
    min_value, min_team = 10000000000, []
    for i in range(process_num):
        if return_dict[i][0] < min_value:
            min_value, min_team = return_dict[i][0], return_dict[i][1]
    print(min_value, min_team)
    v.reset_color_and_edge()
    for e in min_team:
        v.edges[e].add_value(v.edges[e].can_add())
        if v.no_update():
            break
    for node in v.nodes:
        if node.is_tight():
            node.color = 'OrangeRed'
    if draw:
        v.print_map(draw_edge=True, figure_size=figure_size, name=1)
    return min_value


def recursive_calc(v, e):
    v.edges[e].add_value(v.edges[e].can_add())
    if v.no_update():
        cost = 0
        for node in v.nodes:
            if node.is_tight():
                cost += node.cost
        return cost, v
    else:
        min_value, min_v = 0, None
        for next_e in range(len(v.edges)):
            if v.edges[next_e].can_add() > 0:
                v_value, last_v = recursive_calc(copy.deepcopy(v), next_e)
                if v_value > min_value:
                    min_value, min_v = v_value, last_v
        return min_value, min_v


def calc_1(index, v, return_dict):
    v_value, last_v = recursive_calc(copy.deepcopy(v), index)
    return_dict[index] = (v_value, last_v)


def price_recursive(node_num, figure_size, v=None, draw=False):
    if not v:
        v = VertexCover(node_num)
    process_list = []
    manager = Manager()
    return_dict = manager.dict()
    for next_e in range(len(v.edges)):
        p = Process(target=calc_1, args=(next_e, copy.copy(v), return_dict,))  # 实例化进程对象
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
    min_value, min_v = 0, copy.copy(v)
    for next_e in range(len(v.edges)):
        if return_dict[next_e][0]>min_value:
            min_value, min_v = return_dict[next_e][0], return_dict[next_e][1]
    cost = 0
    for node in min_v.nodes:
        if node.is_tight():
            node.color = 'OrangeRed'
            cost += node.cost
    if draw:
        min_v.print_map(draw_edge=True, figure_size=figure_size, name=1)
    return cost


if __name__ == '__main__':
    price_recursive(8, 5, draw=True)
