from assignment8.BuildMap import VertexCover
from assignment8.PriceMethod import price
from assignment8.SetCover import brute, greedy

if __name__ == '__main__':
    last = 0
    # while True:
    #     v = VertexCover(5)
    #     cb = brute(10, 6, v=v)
    #     v.reset_color_and_edge()
    #     cp = price(10, 6, v=v)
    #     v.reset_color_and_edge()
    #     last = max(last, cp / cb)
    #     print('\r{}'.format(last), end='')
    #     if cp / cb >= 2:
    #         break
    v = VertexCover(8)
    cb = greedy(12, 6, v=v, draw=True)
    v.reset_color_and_edge()
    v = VertexCover(8)
    cp = price(12, 6, v=v, draw=True)
    print(cb, cp)
    # greedy(12, 6)
