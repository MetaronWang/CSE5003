import json

import matplotlib.pyplot as plt


def printPic(path, dis, type='NNG', storage_path='./'):
    ps = json.loads(open(storage_path + 'points.json', 'r').read())
    p1 = []
    p2 = []
    for p in ps:
        p1.append(p[0])
        p2.append(p[1])
    plt.figure('Draw')
    x0, x1 = plt.axes().get_xlim()
    y0, y1 = plt.axes().get_ylim()
    plt.axes().set_aspect(abs(x1 - x0) / abs(y1 - y0))
    plt.scatter(p1, p2)  # scatter绘制散点图
    plt.plot(p1[path[0]], p2[path[0]], marker='p', color='r', markersize=10)
    plt.plot([p1[i] for i in path], [p2[i] for i in path])
    plt.text(20, -20, "This is a scheme planned by {}\n"
                      "the total distance is {}".format(type, round(dis, 2)),
             color='red')
    plt.text(p1[path[0]], p2[path[0]], "Start", color='green', fontdict={'size': 20})
    plt.savefig(storage_path + type + '.svg', format='svg')
    plt.clf()


def statistic():
    fig, ax1 = plt.subplots(figsize=(15, 6))
    datas = json.loads(open('result/records.json', 'r').read())
    brute = [i['brute'] for i in datas]
    NNG = [i['NNG'] for i in datas]
    quality = [i['quality'] for i in datas]
    x = list(range(len(NNG)))
    total_width, n = 0.6, 2
    width = total_width / n
    ax1.axis([-1, len(NNG), 200, max([max(NNG), max(brute)]) * 1.1])
    bar1 = ax1.bar(x, brute, width=width, label='brute distance', fc='#60acfc')
    for i in range(len(x)):
        x[i] = x[i] + width
    bar2 = ax1.bar(x, NNG, width=width, label='NGG distance',
                   tick_label=['' if i % 5 > 0 else i for i in range(1, len(NNG) + 1)], fc='#5bc49f')
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.axis([-1, len(NNG), 0.5, max(quality) * 1.1])
    plot = ax2.plot(x, quality, color='#ff7c7c', linewidth=5, label='solution quality', )
    lines = [bar1, bar2] + plot
    ax1.legend(lines, [l.get_label() for l in lines], fontsize= 15, loc='upper left')
    plt.savefig('statistic.jpg', dpi=1000)
    plt.show()


if __name__ == '__main__':
    # printPic([0, 5, 7, 9, 1, 6, 2, 4, 3, 8, 0], 372.1505485558818, 'Brute', './')
    statistic()
