import random

from assignment8.BuildMap import VertexCover


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
