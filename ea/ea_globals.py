from __future__ import division
from collections import namedtuple
from operator import attrgetter
import math

ga_t   = namedtuple('ga_t', ['gtype', 'age'])
gpa_t  = namedtuple('gpa_t', ['gtype', 'ptype', 'age'])
gpfa_t = namedtuple('gpfa_t', ['gtype', 'ptype', 'fitness', 'age'])

def most_fit(population):
    '''Return the most fit individual in the given population'''
    return max(population, key=attrgetter('fitness'))
        
def avg_fitness(population):
    '''Return the average fitness of the population'''
    return sum(ind.fitness for ind in population) / len(population)

def fitness_stddev(population):
    '''Return the standard deviation of the fitnesses in the population'''
    avg = avg_fitness(population)
    return math.sqrt(sum((ind.fitness - avg)**2 for ind in population))
