from scipy import optimize
import numpy as np
from assignment9.BuildMap import VertexCover


def lp(node_num, figure_size, v=None, draw=False):
    if not v:
        v = VertexCover(node_num)
    weights = [node.cost for node in v.nodes]
    A = np.zeros((len(v.edges), node_num))
    node_index = {}
    for i in range(len(v.nodes)):
        node_index[v.nodes[i]] = i
    for e in range(len(v.edges)):
        A[e, node_index[v.edges[e].nodes[0]]] = -1
        A[e, node_index[v.edges[e].nodes[1]]] = -1
    b = -np.ones(len(v.edges))
    res = optimize.linprog(c=weights, A_ub=A, b_ub=b, bounds=[(0, 1) for i in range(node_num)])
    x = res['x']
    all_cost = 0
    for i in range(len(v.nodes)):
        if x[i] > 0.49:
            v.nodes[i].color = 'OrangeRed'
            all_cost += weights[i]
    if draw:
        v.print_map(figure_size=figure_size, name=4)
    return all_cost


if __name__ == '__main__':
    lp(8, 5, draw=True)
