import json
from pathlib import Path
import imageio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from multiprocessing import Process

from PIL import Image


def statistic():
    plt.clf()
    data = json.loads(open('result/statistic.json', 'r').read())
    quality = [i[0] / i[1] for i in data]
    plt.hist(x=quality, bins=80, color='MediumSpringGreen', alpha=0.7, rwidth=0.8)
    plt.xlabel('(center solution/partition solution) Range')
    plt.ylabel('Number')
    plt.savefig('result/rate.jpg', dpi=1000)


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def print_pic(map, centers, u, m, region, name, dpi=100):
    plt.clf()
    plt.grid()
    # plt.figure(figsize=(20, 20))
    plt.axis([1, region + 1, 1, region + 1])
    plt.xticks(range(0, region + 1))
    plt.yticks(range(0, region + 1))
    # u_t = [[u[i][j] for i in range(len(map))]for j in range(len(centers))]
    pca = PCA(n_components=3)
    pca.fit(u)
    u_t = pca.transform(u)
    u_t = normalization(np.array(u_t))
    plt.scatter([i[0] for i in map], [i[1] for i in map], c=u_t, zorder=30, s=[10 for i in range(len(map))])
    plt.scatter([center[0] for center in centers], [center[1] for center in centers], marker='d', color='black',
                s=[100 for i in range(len(centers))],
                zorder=50)
    plt.title('M={}'.format(m))
    # plt.show()
    plt.savefig('result/{}_{}.jpg'.format(name, len(centers)), dpi=dpi)


def print_kmeans_pic(map, centers, clusters, region, name, dpi=100):
    plt.clf()
    plt.grid()
    plt.axis([1, region + 1, 1, region + 1])
    plt.xticks(range(0, region + 1))
    plt.yticks(range(0, region + 1))
    for index in range(len(centers)):
        c = [0 for i in range(len(centers))]
        c[index] = 1
        plt.scatter([site[0] for site in clusters[index]], [site[1] for site in clusters[index]], zorder=20,
                    c=[c for i in range(len(clusters[index]))],
                    s=[20 for i in range(len(clusters[index]))])
    plt.scatter([center[0] for center in centers], [center[1] for center in centers], marker='d', color='black',
                s=[200 for i in range(len(centers))],
                zorder=50)
    plt.savefig('result/{}.jpg'.format(name), dpi=dpi)


def create_gif(path, size, name='cmeans'):
    gif_images = []
    for id in range(size):
        # im = Image.open('result/{}/{}_{}.jpg'.format(path, name, id))
        # im.save('result/{}/{}_{}.jpg'.format(path, name, id), quality=80)
        gif_images.append(imageio.imread('result/{}/{}_{}.jpg'.format(path, name, id)))
    imageio.mimsave("{}_{}.gif".format(name, path), gif_images, fps=6)


if __name__ == '__main__':
    # Process(target=create_gif,args=('center',)).start()
    Process(target=create_gif, args=('u_2', 48)).start()
    # statistic()
