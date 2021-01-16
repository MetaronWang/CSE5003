import random



def gen_map(num, region):
    # random.seed(1000)
    map = []
    while len(map) < num:
        site = [random.randint(1, region), random.randint(1, region)]
        if site not in map:
            map.append(site)
    return map