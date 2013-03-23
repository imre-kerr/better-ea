from __future__ import division
from collections import namedtuple
from operator import attrgetter
import math

class individual:
    def __init__(self, gtype=None, ptype=None, fitness=None, rank=None, distance=None):
        self.gtype = gtype
        self.ptype = ptype
        self.fitness = fitness
        self.rank = rank
        self.distance = distance

def pareto_front(population):
    '''Return the Pareto front or whatever it's called'''
    return [ind for ind in population if ind.rank == 0]
