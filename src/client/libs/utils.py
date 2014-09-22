import math
import random

def getLinearDistributedIndex(size, increasing=False):
    """ Return an index with a linear probability density """
    floatValue = math.sqrt(random.random() * size ** 2)
    if not increasing:
        floatValue = size - floatValue
    return int(math.floor(floatValue))


def probability(prob):
    """ Return true with probability of prob """
    return random.random() < prob
