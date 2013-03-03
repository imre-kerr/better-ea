from ea_globals import *
from sys import stdout
import copy

def gen_mix(new, prev):
    '''Create the next generation by mixing children and adults, add 1 to adults' age'''
    for ind in prev:
        ind.age += 1
    return new + prev
    
def done(pop, goal):
    '''Check if the highest fitness in the population is >= the fitness goal'''
    return max([ind.fitness for ind in pop]) >= goal

def evolutionary_algorithm(initial, development, fitness_test, 
                           adult_selection, parent_selection, 
                           reproduction, generations, fitness_goal):
    '''Main EA loop. 
    
    Return a list of all generations, each a list of (gtype, ptype, fitness) touples'''
    generation_list = []
    genotypes = initial
    stdout.write("\nProgress: generation ")
    for gen in xrange(generations):
        generation_s = str(gen)
        stdout.write(generation_s)
        developed_population = development(genotypes)
        tested_population = fitness_test(developed_population)
        culled_population = adult_selection(tested_population)
        generation_list += [culled_population]
        if fitness_goal != 0 and done(culled_population, fitness_goal):
            break
        # TODO: Uncomment this if Pauline wills it. Also use retested_population in next line.
        # retested_population = fitness_test(culled_population) # retested_population: [(gtype, ptype, fitness, age) list]
        parents = parent_selection(culled_population)
        offspring = reproduction(parents)
        genotypes = gen_mix(offspring, culled_population)
        stdout.write('\b'*len(generation_s))
    print ""
    return generation_list
