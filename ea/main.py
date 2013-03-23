from ea_globals import *
from sys import stdout
import copy

def crowded_comparison(ind_a, ind_b):
    '''Compare two individuals, preferring the one with the lowest rank, or the one
    with the highest crowding distance if they are the same rank'''
    if ind_a.rank != ind_b.rank:
        return ind_b.rank - ind_a.rank
    else:
        return ind_a.distance - ind_b.distance

def dominates(ind_a, ind_b):
    '''Return True if A dominates B, i.e. some fitness of A is better and none are worse'''
    if ind_a.fitness == ind_b.fitness: # == compares values and not addresses
        return False
    else:
        for i in xrange(len(ind_a.fitness)):
            if ind_a.fitness[i] < ind_b.fitness[i]:
                return False
        return True

def crowding_distance_assignment(front):
    '''Assigns a crowding distance to each individual in front'''
    
def fast_non_dominated_sort(population):
    '''Assigns nondomination ranks in O(MN^2) time, which is fancy'''

def evolutionary_algorithm(initial, develop, fitness_test, reproduce, generations):
    '''Main EA loop. 
    
    Return a list of all generations, each a list of individuals'''
    popsize = len(initial)

    generation_list = []
    parent_population = initial
    child_population = []
    stdout.write("\nProgress: generation ")
    for gen in xrange(generations):
        generation_list += [copy.deepcopy(parent_population)]
        generation_s = str(gen+1)
        stdout.write(generation_s)
        population = parent_population + child_population
        develop(population)
        fitness_test(population)
        fronts = fast_non_dominated_sort(population)
        parent_population = []
        i = 0
        while len(parent_population) + len(fronts[i]) < popsize:
            crowding_distance_assignment(fronts[i])
            parent_population += fronts[i]
            i += 1
        
        stdout.write('\b'*len(generation_s))
    print ""
    return generation_list
