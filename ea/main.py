from __future__ import division
from ea_globals import *
from sys import stdout
import copy

INF = float('Inf')

def crowded_comparison(ind_a, ind_b):
    '''Compare two individuals, preferring the one with the lowest rank, or the one
    with the highest crowding distance if they are the same rank. Used for sorting.'''
    if ind_a.rank != ind_b.rank:
        return ind_b.rank - ind_a.rank
    else:
        if ind_a.distance > ind_b.distance:
            return 1
        elif ind_a.distance < ind_b.distance:
            return -1
        else:
            return 0

def dominates(ind_a, ind_b, maximization):
    '''Return True if A dominates B, i.e. some fitness of A is better and none are worse'''
    if ind_a.fitness == ind_b.fitness: # == compares values and not addresses
        return False
    else:
        for i in xrange(len(ind_a.fitness)):
            if maximization[i]:
                if ind_a.fitness[i] < ind_b.fitness[i]:
                    return False
            else:
                if ind_a.fitness[i] > ind_b.fitness[i]:
                    return False
        return True

def crowding_distance_assignment(front, maximization, limits):
    '''Assign a crowding distance to each individual in front.
    NOTE: max/min and fmin, fmax are hardcoded for min_cog!'''
    for ind in front:
        ind.distance = 0
    num_objectives = len(front[0].fitness)
    for m in xrange(num_objectives):
        objective_getter = (lambda ind: ind.fitness[m])
        front.sort(key=objective_getter, reverse=maximization[m])
        front[0].distance = front[-1].distance = INF
        for i in xrange(1, len(front)-1):
            norm = limits[m][1] - limits[m][0]
            front[i].distance += abs(front[i+1].fitness[m] - front[i-1].fitness[m])/norm

    
def fast_non_dominated_sort(population, maximization):
    '''Assigns nondomination ranks in O(MN^2) time, which is fancy'''
    popsize = len(population)

    # dominated_sets[i] -> the set of indexes to solutions dominated by solution i
    dominated_sets = [[] for i in xrange(popsize)]

    # domination_counts[i] -> number of solutions that dominate solution i
    domination_counts = [0]*popsize

    fronts = [[]]

    for p in xrange(popsize):
        for q in xrange(popsize):
            if dominates(population[p], population[q], maximization):
                dominated_sets[p].append(q)
            elif dominates(population[q], population[p], maximization):
                domination_counts[p] += 1
        if domination_counts[p] == 0:
            population[p].rank = 0
            fronts[0].append(population[p])
    i = 0
    while fronts[i]:
        next_front = []
        for p in xrange(len(fronts[i])):
            for q in xrange(popsize):
                domination_counts[q] -= 1
                if domination_counts[q] == 0:
                    population[q].rank = i + 1
                    next_front.append(population[q])
        i += 1
        fronts.append(next_front)
    return fronts

def evolutionary_algorithm(initial, develop, fitness_test, reproduce, 
                           select_parents, generations, maximization, limits):
    '''Main EA loop. 
    
    Return a list of all generations, each a list of individuals'''
    popsize = len(initial)

    generation_list = []
    parent_population = initial
    child_population = []

    stdout.write("\nProgress: generation ")

    for gen in xrange(generations):
        generation_s = str(gen+1)
        stdout.write(generation_s)

        population = parent_population + child_population
        develop(population)
        fitness_test(population)
        fronts = fast_non_dominated_sort(population, maximization)
        parent_population = []
        i = 0
        while len(parent_population) + len(fronts[i]) < popsize:
            crowding_distance_assignment(fronts[i], maximization, limits)
            parent_population += fronts[i]
            i += 1
        crowding_distance_assignment(fronts[i], maximization, limits)
        fronts[i].sort(reverse=True, cmp=crowded_comparison)
        parent_population += fronts[i][:popsize-len(parent_population)]
        generation_list += [copy.deepcopy(parent_population)]
        parent_list = select_parents(parent_population)
        child_population = reproduce(parent_list)

        stdout.write('\b'*len(generation_s))
    print ""
    return generation_list
