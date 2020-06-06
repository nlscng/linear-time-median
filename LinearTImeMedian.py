# GG: from omscs lecture here https://classroom.udacity.com/courses/ud401/lessons/10090188016/concepts/100938679580923
import random
import time

GROUP_SIZE = 5


def linear_time_kth_smallest(arr: list, k: int) -> int:
    if k >= len(arr):
        raise Exception('K is larger than size of array')

    if len(arr) < GROUP_SIZE:
        return sorted(arr)[k]

    meds = []
    walker = 0
    while walker < len(arr):
        each_group = arr[walker: walker + GROUP_SIZE] if walker < len(arr) - GROUP_SIZE else arr[walker:]
        meds.append(sorted(each_group)[len(each_group) // 2])
        walker += GROUP_SIZE

    pivot = linear_time_kth_smallest(meds, len(arr) // (2 * GROUP_SIZE))

    lesser, equals, greater = [], [], []
    for a in arr:
        if a < pivot:
            lesser.append(a)
        elif a > pivot:
            greater.append(a)
        else:
            equals.append(a)

    if k < len(lesser):
        return linear_time_kth_smallest(lesser, k)
    elif len(lesser) <= k < len(lesser) + len(equals):
        return pivot
    else:
        return linear_time_kth_smallest(greater, k - len(lesser) - len(equals))


random.seed(42)
# t1 = random.sample(range(GROUP_SIZE * 10), 2 * GROUP_SIZE)
t10 = [40, 7, 1, 17, 15, 14, 8, 6, 34, 5]  # sorted: [1, 5, 6, 7, 8, 15, 17, 34, 40]
k_idx_smallest = 3
assert linear_time_kth_smallest(t10, k_idx_smallest) == 7, "Actual: {}".format(
    linear_time_kth_smallest(t10, k_idx_smallest))

k_idx_smallest = 8
assert linear_time_kth_smallest(t10, k_idx_smallest) == 34
assert linear_time_kth_smallest(t10, 0) == 1

t100 = random.sample(range(GROUP_SIZE * 100), 20 * GROUP_SIZE)
t100_sorted = sorted(t100)
k_idx_smallest = 42
assert linear_time_kth_smallest(t100, k_idx_smallest) == t100_sorted[k_idx_smallest]


def repeat_for_size(sizes: list):
    n = len(sizes)
    assert n > 1
    num_reps = 1000
    run_times = []

    for one_size in sizes:
        assert one_size >= 100 and one_size % 100 == 0
        start = time.time_ns()
        for i in range(num_reps):
            arr = random.sample(range(GROUP_SIZE * one_size), one_size)
            random_k = random.randint(1, one_size) - 1
            linear_time_kth_smallest(arr, random_k)
        end = time.time_ns()
        print("Size of {} for linear time k-th smallest took {} ms".format(one_size, (end - start) // 1000))
        run_times.append(end - start)

    base_time = run_times[0]
    tolerance = 0.08
    for idx in range(1, n):
        size_ratio = float(sizes[idx]) / sizes[0]
        time_ratio = run_times[idx] / base_time
        print('Time ratio for {} times the size is {}.'.format(time_ratio, size_ratio))
        assert (1 - tolerance) * size_ratio < time_ratio < (1 + tolerance) * size_ratio


repeat_for_size([(x + 1) * 100 for x in range(10)])
