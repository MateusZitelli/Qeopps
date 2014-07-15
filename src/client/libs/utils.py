import math
import random

def getLinearDistributedIndex(size):
  return int( math.floor( math.sqrt( random.random() * size ** 2)))

def probability(prob):
  return random.random() < prob
