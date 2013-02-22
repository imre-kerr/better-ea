from ea import adult_selection
from ea import parent_selection
from ea import reproduction
from ea import main
from ea import binary_gtype

def fitness_test(population):
    '''Naive fitness test for onemax, just the number of ones'''
    return [(ind[0], ind[1], sum(ind[1]), ind[2]) for ind in population]

def develop(population):
    '''Development function for onemax (just copies the genotype)'''
    return [(ind[0], list(ind[0]), ind[1]) for ind in population]

def visualize(generation_list):
    '''Generate visualizations using matplotlib'''
    return None

if __name__=='__main__':
    size = int(raw_input("Input problem size: "))
    popsize = int(raw_input("Input population size: "))

    adult_selection, litter_size = adult_selection.gen_adult_selection(popsize)
    parent_selection = parent_selection.gen_parent_selection(litter_size)

    mutate = binary_gtype.gen_mutate()
    crossover = binary_gtype.gen_crossover()
    reproduction = reproduction.gen_reproduction(mutate, crossover)

    generations = int(input("Input max number of generations: "))
    fitness_goal = float(input("Input fitness goal, 0 for none: "))

    initial = [(binary_gtype.generate(size), 0) for i in xrange(popsize)]
    generation_list = main.evolutionary_algorithm(initial, develop, fitness_test, adult_selection, parent_selection, reproduction, generations, fitness_goal)
