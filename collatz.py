import numba as nb
import time
from matplotlib import pyplot as plt

def time_function(func, args):
    t = time.time()
    val = func(*args)
    return time.time() - t, val

@nb.njit('uint16(uint64)')
def collatz(val):
    i = 0
    # x, y = [], []
    while val != 4:
        i+=1
        # x.append(i), y.append(val)
        if val % 2:
            val = val * 3 + 1
        else:
            val = val // 2
    # return x, y
    return i

if __name__ == '__main__':
    # x, y = collatz(670617279)
    # plt.plot(x, y)
    # plt.show()
    # quit()
    maxes = [0]
    vals = [0]
    low, high = 1000000000, 1000000000  # 670617279 984
    for i in range(low, high):
        length = collatz(i)
        if length > maxes[-1]:
            print(i, length)
            maxes.append(length)
            vals.append(i)
    plt.plot(vals, maxes)
    plt.show()


