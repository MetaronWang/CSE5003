import os
import numpy as np
from assignment1.brute import brute
from assignment1.generateMap import getPoints, getDistance
from assignment1.NNG import NNG
from assignment1.pic import printPic
import json



if __name__ == '__main__':
    all = []
    distance = 1600
    root_dir = "result_{}".format(distance)
    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)
    for i in range(200):
        print(i)
        path = "{}/sample_{}/".format(root_dir, i)
        if not os.path.isdir(path):
            os.mkdir(path)
        getPoints(10, path)
        getDistance(10, path)
        dis_brute, path_brute = brute(path)
        min_NNG, max_NNG = NNG(path)
        dis_NNG, path_NNG = min_NNG
        max_dis_NNG, max_path_NNG = max_NNG
        path_NNG = [int(i) for i in path_NNG]
        path_brute = [int(i) for i in path_brute]
        record = {'brute': dis_brute, 'NNG': dis_NNG,
                  'brute_path': path_brute,
                  'NNG_path': path_NNG,
                  'max_NNG': max_dis_NNG,
                  'max_NNG_path': max_path_NNG,
                  'quality': dis_NNG / dis_brute,
                  'max_quality': max_dis_NNG/ dis_brute
                  }
        all.append(record)
        open(path + 'value.json', 'w').write(json.dumps(record))
        printPic(path_brute, dis_brute, 'brute', path)
        printPic(path_NNG, dis_NNG, 'NNG', path)
        printPic(max_path_NNG, max_dis_NNG, 'max_NNG', path)
    open('{}/records.json'.format(root_dir), 'w').write(json.dumps(all))
