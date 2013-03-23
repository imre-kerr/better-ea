from ea_globals import *
from sys import stdout
import copy

def evolutionary_algorithm(initial, develop, fitness_test, reproduce, generations):
    '''Main EA loop. 
    
    Return a list of all generations, each a list of individuals'''
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
        
        stdout.write('\b'*len(generation_s))
    print ""
    return generation_list
