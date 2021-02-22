from queue import Queue
import logging

from utils import *


def ddmin(c, n, test):
    """
    The original delta debugging algorithm

    :param c: Current input
    :param n: Current granularity
    :param test: Test function used to determine if a particular input leads to a fault, a return value of True
        indicates a failure
    :return: Minimal subset of c leading to a failure
    """

    logger = logging.getLogger('network-testing')
    logger.info(f'\nRunning minimization on set {str_repr(c)} with granularity {n}\n')

    if not n <= len(c):
        return c

    split = [c[i * (len(c) // n) + min(i, len(c) % n):(i + 1) * (len(c) // n) + min(i + 1, len(c) % n)] for i in
             range(n)]

    comps = [[i for i in c if i not in delta] for delta in split]

    for delta in split:
        if test(delta):
            return ddmin(delta, 2, test)

    for comp in comps:
        if test(comp):
            return ddmin(comp, max(n - 1, 2), test)

    if n < len(c):
        return ddmin(c, min(len(c), 2 * n), test)
    else:
        return c


def ddmin_iter(c, test_f, test_tc, f_to_tc):
    """
    Iterative delta debugging algorithm
    :param c: Starting input
    :param test_f: Higher level test function
    :param test_tc: Lower level test function
    :param f_to_tc: Function to convert from high to low level
    :return: A list of minimal failure-inducing subsets for c
    """
    logger = logging.getLogger('network-testing')

    min_sets = []
    q = Queue()
    q.put(c)

    while not q.empty():
        h = q.get()
        faulty_feature_set = False
        for ms in min_sets:
            if all([f in f_to_tc(h) for f in ms]):
                for f in ms:
                    q.put([x for x in h if x != f])
                faulty_feature_set = True
                break
        if faulty_feature_set:
            continue

        if test_f(h):
            min_features = ddmin(h, 2, test_f)
            min_set = ddmin(f_to_tc(min_features), 2, test_tc)
            logger.info(f'New minimal subset: {str_repr(min_set)}\n')
            min_sets.append(min_set)

            for f in min_features:
                q.put([x for x in h if x != f])

    return min_sets
