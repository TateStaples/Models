from numba import jit
import time

def time_function(func, args, count=1):
    # print(args, count)
    t = time.time()
    for i in range(count):
        func(*args)
    return time.time() - t

@jit(nopython=True)
def step(time, predators, prey):
    # constants
    prey_fecundity = 0.05
    capacity = 5000
    deaths_per_pred = 0.001
    hunt_rate = 0.0002
    pred_starvation_rate = 0.03

    # derivatives
    predators, prey = \
        predators + (hunt_rate * predators * prey - pred_starvation_rate * predators) * time, \
        prey + (prey_fecundity * prey * (1-prey/capacity) - deaths_per_pred * predators * prey) * time

    # return all variables
    return predators, prey

@jit(nopython=True)
def run(time, timestep, pred, prey):
    t = 0
    # counts = list()
    while t < time:
        # if int(t) == t:
        #     counts.append((pred, prey))
        pred, prey = step(timestep, pred, prey)
        t += timestep
    # return counts


if __name__ == '__main__':
    run(2, 1, 1, 1)
    print(time_function(run, [200000, 0.0001, 40, 200], count=1))

