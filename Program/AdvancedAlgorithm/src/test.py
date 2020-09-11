
a = [1,23,4,5,6]
b = [4]
if __name__ == '__main__':
    a1 = a.copy()
    a1.remove(4)
    print(a1)
    print(a)
    print(b)