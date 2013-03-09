from functools import partial

from ea import adult_selection
from ea import parent_selection
from ea import reproduction
from ea import float_gtype
from ea import main
from ea.ea_globals import *

import ctrnn
import min_cog_game

def fitness_test(population, visual):
    '''Play a game with each individual in the population and assign fitness based on score'''
    game = min_cog_game.Game()
    for ind in population:
        if visual:
            score = game.play_visual(ind.ptype)
        else:
            score = game.play(ind.ptype)
        ind.fitness = max(0, score)
    return population
    
def gen_fitness():
    '''Generate the fitness function interactively'''
    while True:
        visual = raw_input("Do you want gameplay visualisations? (y/n):\n")
        if visual == 'y' or visual == 'Y':
            return partial(fitness_test, visual=True)
        elif visual == 'n' or visual == 'N':
            return partial(fitness_test, visual=False)
        else:
            print "Please type y or n."
    
def develop(population, num_input, num_hidden, num_output):
    '''Create CTRNN objects from float lists.'''
    num_weights = num_hidden*(num_input + num_hidden) + num_output*(num_hidden + num_output)
    num_biases = num_hidden + num_output
    num_gains = num_hidden + num_output
    num_taus = num_hidden + num_output
    
    for ind in population:
        print len(ind.gtype)
        i = 0
        weight_list = ind.gtype[i:i+num_weights]
        i += num_weights
        bias_list = ind.gtype[i:i+num_biases]
        i += num_biases
        gain_list = ind.gtype[i:i+num_gains]
        i += num_gains
        tau_list = ind.gtype[i:i+num_taus]
        ind.ptype = ctrnn.CTRNN(num_input, num_hidden, num_output, 
                                weight_list, bias_list, gain_list, tau_list)
    return population
        
if __name__ == "__main__":
    popsize = int(raw_input("Input population size:\n"))
    
    adult_selector, litter_size = adult_selection.gen_adult_selection(popsize)
    parent_selector = parent_selection.gen_parent_selection(litter_size)
 
    num_input = 5
    num_hidden = 2
    num_output = 2
    num_weights = num_hidden*(num_input + num_hidden) + num_output*(num_hidden + num_output)
    num_biases = num_hidden + num_output
    num_gains = num_hidden + num_output
    num_taus = num_hidden + num_output
 
    ranges = []
    ranges += [(-5.0, 5.0)]*num_weights 
    ranges += [(-10.0, 0.0)]*num_biases
    ranges += [(1.0, 5.0)]*num_gains
    ranges += [(1.0, 2.0)]*num_taus
       
    mutate = float_gtype.gen_mutate(ranges)
    crossover = float_gtype.gen_crossover()
    reproducer = reproduction.gen_reproduction(mutate, crossover)

    generations = int(raw_input("Input max number of generations:\n"))
    fitness_goal = float(raw_input("Input fitness goal, 0 for none:\n"))
    
    development = partial(develop, num_input=num_input, num_hidden=num_hidden, num_output=num_output)
    fitness_tester = gen_fitness()

    initial = [individual(gtype=float_gtype.generate(ranges), age=0) for i in xrange(popsize)]
    
    generation_list = main.evolutionary_algorithm(initial, development, fitness_tester, adult_selector, parent_selector, reproducer, generations, fitness_goal)