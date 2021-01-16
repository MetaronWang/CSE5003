from assignment9.BuildMap import VertexCover
from assignment9.PriceMethod import price, price_parallel, price_recursive
from assignment9.SetCover import brute, greedy
from assignment9.LP import lp

if __name__ == '__main__':
    last = 0
    node_num = 7
    while True:
        v = VertexCover(node_num)
        cg = greedy(node_num, 6, v=v)
        v.reset_color_and_edge()
        cp = price_recursive(node_num, 6, v=v)
        v.reset_color_and_edge()
        cl = lp(node_num, 6, v=v)
        v.reset_color_and_edge()
        last = max(last, min(cg / cp, cl / cp))
        print('\r{}'.format(last), end='')
        if last > 1.000001:
            break
    print('\nFind')
    v.reset_color_and_edge()
    cg = greedy(node_num, 6, v=v, draw=True)
    v.reset_color_and_edge()
    cp = price_recursive(node_num, 6, v=v, draw=True)
    v.reset_color_and_edge()
    cl = lp(node_num, 6, v=v, draw=True)
    print(cg, cp, cl)
    m, v = v.build_wolfram_data()
    print(m)
    print(v)
