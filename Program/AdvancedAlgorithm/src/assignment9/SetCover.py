import random
from itertools import combinations

from assignment9.BuildMap import VertexCover


def brute(node_num, figure_size, v=None, draw=False):
    if not v:
        v = VertexCover(node_num)
    min_value, min_team = 10000000000, []
    edge_dict = {}
    for i in range(len(v.edges)):
        edge_dict[v.edges[i]] = i
    for i in range(len(v.nodes)):
        xx = list(combinations(range(len(v.nodes)), i + 1))
        for m in xx:
            task_count = [0 for i in range(len(v.edges))]
            for index in m:
                for t in v.nodes[index].edge_list:
                    task_count[edge_dict[t]] += 1
            if 0 not in task_count:
                cost = sum([v.nodes[index].cost for index in m])
                if cost < min_value:
                    min_value, min_team = cost, m
    for index in min_team:
        v.nodes[index].color = 'OrangeRed'
    if draw:
        v.print_map(figure_size=figure_size, name=3)
    return min_value


def greedy(node_num, figure_size, v=None, draw=False):
    if not v:
        v = VertexCover(node_num)
    r = {i for i in v.edges}
    m = {i for i in v.nodes}
    s = []
    cost = 0
    while len(r) > 0:
        choice = min(m, key=lambda item: item.cost / max(len(r & set(item.edge_list)) * 1.0, 0.001))
        s.append(choice)
        for i in choice.edge_list:
            if i in r:
                r.remove(i)
        m.remove(choice)
    for node in s:
        node.color = 'OrangeRed'
        cost += node.cost
    if draw:
        v.print_map(figure_size=figure_size, name=2)
    return cost


if __name__ == '__main__':
    greedy(8, 5, draw=True)
