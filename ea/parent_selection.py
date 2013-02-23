from __future__ import division
from bisect import bisect_left
from named_tuples import *
from operator import attrgetter
import random
import math


def roulette(prob_list):
    '''TODO: Explain this shit'''
    cumulative = [prob_list[i] + sum(prob_list[:i]) for i in xrange(len(prob_list))]
    randval = random.random() * cumulative[-1]
    return bisect_left(cumulative, randval)

def stochastic_uniform(population, litter_size):
    '''Choose parents with equal probability'''
    return [(random.choice(population).gtype, random.choice(population).gtype) for i in xrange(litter_size)]
    
def fitness_proportionate(population, litter_size):
    '''Choose parents with probability proportional to their fitness'''
    fitness_list = [ind.fitness for ind in population]
    gtype_list = [ind.gtype for ind in population]

    parents = []
    for i in xrange(litter_size):
        parents += [(gtype_list[roulette(fitness_list)], gtype_list[roulette(fitness_list)])]
    return parents

def sigma_scaling(population, litter_size):
    '''Choose parents with probability proportional to their fitness, scaled by the population's standard deviation'''
    fitness_list = [ind.fitness for ind in population]
    gtype_list = [ind.gtype for ind in population]
    avg = sum(fitness_list) / len(fitness_list)
    sigma = math.sqrt(sum([(f - avg)**2 for f in fitness_list]))

    if sigma != 0:
        scaled_fitness = [1 + (f - avg)/(2*sigma) for f in fitness_list]
    else:
        scaled_fitness = [1] * len(fitness_list)

    parents = []
    for i in xrange(litter_size):
        parents += [(gtype_list[roulette(fitness_list)], gtype_list[roulette(fitness_list)])]
    return parents

def tournament(population, litter_size, tournament_size):
    '''Choose parents by choosing the most fit individual from a tournament_size size random sample of the population'''
    parents = []
    for i in xrange(litter_size):
        t1 = random.sample(population, tournament_size)
        t2 = random.sample(population, tournament_size)
        p1 = max(t1, key=attrgetter('fitness'))
        p2 = max(t2, key=attrgetter('fitness'))
        parents += [(p1.gtype, p2.gtype)]
    return parents

def gen_parent_selection(litter_size):
    '''Generate a parent selection function interactively'''
    while True:
        method = raw_input("Input parent selection mechanism (uniform/proportionate/sigma/tournament):\n")
        if method == 'uniform':
            return (lambda population: stochastic_uniform(population, litter_size))
        elif method == 'proportionate':
            return (lambda population: fitness_proportionate(population, litter_size))
        elif method == 'sigma':
            return (lambda population: sigma_scaling(population, litter_size))
        elif method == 'tournament':
            tournament_size = int(raw_input("Input tournament size:\n"))
            return (lambda population: tournament(population, litter_size, tournament_size))
        else:
            print "Unrecognized method: " + method + "\n"
