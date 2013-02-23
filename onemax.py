from ea import adult_selection
from ea import parent_selection
from ea import reproduction
from ea import main
from ea import binary_gtype
from ea.named_tuples import *

def fitness_test(population):
    '''Naive fitness test for onemax, just the number of ones'''
    tested = []
    for ind in population:
        tested += [gpfa_t(gtype=ind.gtype, ptype=ind.ptype, fitness=sum(ind.ptype), age=ind.age)]
    return tested

def develop(population):
    '''Development function for onemax (just copies the genotype)'''
    developed = []
    for ind in population:
        developed += [gpa_t(gtype=ind.gtype, ptype=list(ind.gtype), age=ind.age)]
    return developed

def visualize(generation_list):
    '''Generate visualizations using matplotlib'''
    return None

if __name__=='__main__':
    size = int(raw_input("Input problem size:\n"))
    popsize = int(raw_input("Input population size:\n"))

    adult_selection, litter_size = adult_selection.gen_adult_selection(popsize)
    parent_selection = parent_selection.gen_parent_selection(litter_size)

    mutate = binary_gtype.gen_mutate()
    crossover = binary_gtype.gen_crossover()
    reproduction = reproduction.gen_reproduction(mutate, crossover)

    generations = int(input("Input max number of generations:\n"))
    fitness_goal = float(input("Input fitness goal, 0 for none:\n"))

    initial = [ga_t(gtype=binary_gtype.generate(size), age=0) for i in xrange(popsize)]
    generation_list = main.evolutionary_algorithm(initial, develop, fitness_test, adult_selection, parent_selection, reproduction, generations, fitness_goal)

    print "Program ran for " + str(len(generation_list)) + " generations"
