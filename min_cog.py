from functools import partial
import copy
import pylab
import multiprocessing as mp

from ea import adult_selection
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
    
def fitness_test_mp(population, game):
    '''Multiprocessing fitness test'''
    games = [copy.deepcopy(game) for i in xrange(len(population))]
    pool = mp.Pool(mp.cpu_count())
    indices = []
    workers = []
    for i, ind in enumerate(population):
        indices += [i]
        workers += [pool.apply_async(fitness_thread, [ind.ptype, games[i]])]
    for i, worker in enumerate(workers):
        score = worker.get()
        if population[indices[i]].fitness:
            population[indices[i]].fitness = (population[indices[i]].fitness + score)/2.
        else:
            population[indices[i]].fitness = max(0, score)
    pool.close()
    pool.join()
    return population
    

def fitness_test(population, visual):
    '''Play a game with each individual in the population and assign fitness based on score'''
    game = min_cog_game.Game()
    if visual:
        for ind in population:
            score = game.play(ind.ptype, visual)
            ind.fitness = max(0, score)
        return population
    else:
        return fitness_test_mp(population, game)
    
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
        
def visualize(generation_list):
    '''Generate pretty pictures using pylab and pygame'''
    best = []
    average = []
    stddev = []
    average_plus_stddev = []
    average_minus_stddev = []
    for pop in generation_list:
        best += [most_fit(pop).fitness]
        average += [avg_fitness(pop)]
        stddev += [fitness_stddev(pop)] 
        average_plus_stddev += [average[-1] + stddev[-1]]
        average_minus_stddev += [average[-1] - stddev[-1]]
    
    pylab.figure(1)
    pylab.fill_between(range(len(generation_list)), average_plus_stddev, average_minus_stddev, alpha=0.2, color='b', label="Standard deviation")
    pylab.plot(range(len(generation_list)), best, color='r', label='Best')
    pylab.plot(range(len(generation_list)), average, color='b', label='Average with std.dev.')
    pylab.title("Fitness plot - Beer-cog")
    pylab.xlabel("Generation")
    pylab.ylabel("Fitness")
    pylab.legend(loc="upper left")
    pylab.savefig("mincog_fitness.png")

    best_index = best.index(max(best))
    best_individual = most_fit(generation_list[-1])

    with open('last.txt','w') as f:
        f.write(str(best_individual.gtype))
    print best_individual.gtype
    
    game = min_cog_game.Game()
    game.play(best_individual.ptype, True)
    
        
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
    
    visualize(generation_list)