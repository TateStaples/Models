from random import *
from time import time


def merge_sort(stuff):
    if len(stuff) == 1:
        return stuff
    half_way_point = len(stuff)//2
    half1 = merge_sort(stuff[:half_way_point])
    half2 = merge_sort(stuff[half_way_point:])
    new_list = []
    while len(half1) > 0 and len(half2) > 0:
        thing1 = half1[0]
        thing2 = half2[0]
        if thing1 < thing2:
            new_list.append(half1.pop(0))
        else:
            new_list.append(half2.pop(0))
    new_list.extend(half1)
    new_list.extend(half2)
    return new_list


def bubble_sort(stuff):
    for iteration in range(len(stuff) - 1):
        for index in range(len(stuff) - iteration - 1):
            thing1 = stuff[index]
            thing2 = stuff[index+1]
            if thing1 > thing2:
                stuff[index] = thing2
                stuff[index+1] = thing1
    return stuff


def insertion_sort(stuff):
    for key in range(1, len(stuff)):
        print(stuff)
        thing1 = stuff[key]
        for spot in reversed(range(0, key)):
            thing2 = stuff[spot]
            if thing1 >= thing2:
                stuff.insert(spot+1, stuff.pop(key))
                break
        else:
            stuff.insert(0, stuff.pop(key))
    return stuff


def quick_sort(stuff):
    if len(stuff) <= 1:
        #print(stuff)
        return stuff
    pivot_index = len(stuff) // 2
    thing1 = stuff[pivot_index]
    lower_list = []
    higher_list = []
    for i in range(len(stuff)):
        thing2 = stuff[i]
        if i == pivot_index:
            continue
        if thing2 > thing1:
            higher_list.append(thing2)
        else:
            lower_list.append(thing2)
    sort1 = quick_sort(lower_list)
    sort1.append(thing1)
    sort2 = quick_sort(higher_list)
    sort1.extend(sort2)
    return sort1


def selection_sort(stuff):
    for start_index in range(len(stuff)):
        lowest = min(stuff[start_index:])
        low_index = stuff.index(lowest, start_index)
        stuff.pop(low_index)
        stuff.insert(start_index, lowest)
    return stuff


def heap_sort(stuff):
    pass


def counting_sort(stuff):
    pass


def seperation_sort(stuff):
    new_list = []
    for thing in stuff:
        new_list.insert(binary_search(thing, new_list), thing)
    return new_list


def binary_search(key, compare_list):
    low = 0
    high = len(compare_list)
    if high == 0:
        return 0
    while high - low > 1:
        average = (high + low) // 2
        thing = compare_list[average]
        if thing == key:
            return average
        if thing > key:
            high = average
        else:
            low = average
    if compare_list[low] >= key:
        return low
    return high


def bogosort(stuff):
    while True:
        shuffle(stuff)
        max = stuff[0]
        for thing in stuff:
            if thing > max:
                max = thing
            elif thing < max:
                break
        else:
            break
    return stuff


if __name__ == '__main__':
    size = 10
    top = 10
    test_list = [randint(0, top) for i in range(size)]
    start_time = time()
    print(insertion_sort(test_list))
    print(time()-start_time)

'''
Round 1:
Parameters: list size = 10000, max = 100000
bubble = 1) 8.46, 2) 8.02, 3) 8.15. 4) 8.40, 5) 8.66
merge = 1) 0.08, 2) 0.08, 3) 0.07, 4) 0.07, 5) 0.07
insertion = 1) 1.69, 2) 1.97, 3) 1.90, 4) 1.81, 5) 1.82
quick = 1) 0.05, 2) 0.04, 3) 0.04, 4) 0.04, 5) 0.04
selection = 1) 1.42, 2) 1.64, 3) 1.54, 4) 1.61, 5) 1.56
seperation = 1) 0.04, 2) 0.04, 3) 0.04, 4) 0.04, 5) 0.04
winners: merge, quick, seperation

Round 2:
Parameters: list size = 100000, max = 1000000
merge = 1) 1.67, 2) 1.96, 3) 1.61, 4) 1.95, 5) 1.99
quick = 1) 0.42, 2) 0.40, 3) 0.46, 4) 0.44, 5) 0.44
separation = 1) 1.54, 2) 1.37, 3) 1.36, 4) 1.51, 5) 1.49
winner: quick sort
'''