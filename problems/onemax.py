from ea import autogen
from ea import main
from ea import binary_gtype

def fitness_test(population):
    '''Naive fitness test for onemax, just the number of ones'''
    return [ind[0], ind[1], sum(ind[1]), ind[2] for ind in population]

def develop(population):
    '''Development function for onemax (just copies the genotype)'''
    return [ind[0], ind[0].copy(), ind[1] for ind in population]

def visualize(generation_list):
    '''Generate visualizations using matplotlib'''

if __name__=='__main__':
    size = int(raw_input("Input problem size: "))
    popsize, adult_selection, parent_selection, reproduction, generations, fitness_goal = autogen.generate()
    initial = [binary_gtype.generate(size), 0 for i in xrange(popsize)]
    generation_list = main.evolutionary_algorithm(initial, develop, fitness_test, adult_selection, parent_selection, reproduction, generations, fitness_goal)
