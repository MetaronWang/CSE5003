import os
import numpy as np
from assignment1.brute import brute
from assignment1.generateMap import getPoints, getDistance
from assignment1.NNG import NNG
from assignment1.pic import printPic
import json


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


if __name__ == '__main__':
    all = []
    for i in range(40):
        print(i)
        path = "result/sample_" + str(i) + "/"
        if not os.path.isdir(path):
            os.mkdir(path)
        getPoints(10, path)
        getDistance(10, path)
        dis_brute, path_brute = brute(path)
        dis_NNG, path_NNG = NNG(path)
        path_NNG = [int(i) for i in path_NNG]
        path_brute = [int(i) for i in path_brute]
        record = {'brute': dis_brute, 'NNG': dis_NNG,
                  'brute_path': path_brute,
                  'NNG_path': path_NNG,
                  'quality': dis_NNG / dis_brute}
        all.append(record)
        open(path + 'value.json', 'w').write(json.dumps(record))
        printPic(path_brute, dis_brute, 'brute', path)
        printPic(path_NNG, dis_NNG, 'NNG', path)
    open('result/records.json', 'w').write(json.dumps(all))
