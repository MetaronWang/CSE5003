import json
from pathlib import Path
import imageio
import matplotlib.pyplot as plt
from multiprocessing import Process

def statistic():
    plt.clf()
    data = json.loads(open('result/statistic.json', 'r').read())
    quality = [i[0]/i[1] for i in data]
    plt.hist(x=quality, bins=80, color='MediumSpringGreen', alpha=0.7, rwidth=0.8)
    plt.xlabel('(center solution/partition solution) Range')
    plt.ylabel('Number')
    plt.savefig('result/rate.jpg', dpi=1000)

def print_pic(map, centers, clusters, region, name):
    plt.clf()
    plt.grid()
    plt.figure(figsize=(20, 20))
    plt.axis([1, region + 1, 1, region + 1])
    plt.xticks(range(0, region + 1))
    plt.yticks(range(0, region + 1))
    for index in range(len(centers)):
        for site in clusters[index]:
            plt.plot([centers[index][0], site[0]], [centers[index][1], site[1]], color='g')
    plt.scatter([i[0] for i in map], [i[1] for i in map], zorder=30)
    plt.scatter([center[0] for center in centers], [center[1] for center in centers], color='r', s=10, zorder=50)
    plt.savefig('result/{}.jpg'.format(name), dpi=100)


def create_gif(path):
    gif_images = []
    for id in range(30):
        gif_images.append(imageio.imread('result/{}/kmeans_{}.jpg'.format(path, id)))
    imageio.mimsave("{}.gif".format(path), gif_images, fps=6)

if __name__ == '__main__':
    # Process(target=create_gif,args=('center',)).start()
    # Process(target=create_gif,args=('cluster',)).start()
    statistic()