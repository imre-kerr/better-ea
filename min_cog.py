from functools import partial
import copy
import pylab
import multiprocessing as mp

from ea import parent_selection
from ea import reproduction
from ea import float_gtype
from ea import main
from ea.ea_globals import *

import ctrnn
import min_cog_game

def fitness_thread(agent, game):
    '''A single fitness testing thread'''
    return game.play(agent, False)
    
def fitness_test_mp(population):
    '''Multiprocessing fitness test'''
    game = min_cog_game.Game()
    games = [copy.deepcopy(game) for i in xrange(len(population))]
    pool = mp.Pool(mp.cpu_count())
    indices = []
    workers = []
    for i, ind in enumerate(population):
        if ind.fitness is not None:
            indices += [i]
            workers += [pool.apply_async(fitness_thread, [ind.ptype, games[i]])]
    for i, worker in enumerate(workers):
        population[indices[i]].fitness = worker.get()
    pool.close()
    pool.join()
    
def fitness_test(population):
    '''Single-processor fitness test (for profiling)'''
    game = min_cog_game.Game()
    for ind in population:
        ind.fitness = game.play(ind.ptype, False)
    return population

def develop(population, num_input, num_hidden, num_output):
    '''Create CTRNN objects from float lists.'''
    num_weights = num_hidden*(num_input + num_hidden) + num_output*(num_hidden + num_output)
    num_biases = num_hidden + num_output
    num_gains = num_hidden + num_output
    num_taus = num_hidden + num_output
    
    for ind in population:
        if ind.ptype is not None:
            continue
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
        
def visualize(generation_list):
    '''Generate pretty pictures using pylab and pygame'''
    game = min_cog_game.Game()
    ctrnn_list = [ind.ptype for ind in pareto_front(generation_list[-1])]
    for ind in pareto_front(generation_list[-1]):
        print ind.fitness
    print "Visualizing " + str(len(ctrnn_list)) + " agents."
    game.play_list(ctrnn_list)
    
        
if __name__ == "__main__":
    popsize = int(raw_input("Input population size:\n"))
    
    parent_selector = parent_selection.gen_parent_selection(popsize)
 
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

    maximization = [True, False]
    limits = [(0, 1), (0, 2400)]

    generations = int(raw_input("Input max number of generations:\n"))
    
    development = partial(develop, num_input=num_input, num_hidden=num_hidden, num_output=num_output)
    
    initial = [individual(gtype=float_gtype.generate(ranges)) for i in xrange(popsize)]
    generation_list = main.evolutionary_algorithm(initial, development, fitness_test_mp, reproducer, parent_selector, generations, maximization, limits)
    
    visualize(generation_list)
