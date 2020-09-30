import json
import random
from pathlib import Path


def generateTask(path, num, upper=100, lower=10):
    task = []
    # for i in range(num):
    #     task.append(random.randint(1, 10))
    task.append(num)
    for i in range(num, num * 2):
        task += [i, i]
    open(Path(path, 'task.json'), 'w').write(json.dumps(task))
    return task
