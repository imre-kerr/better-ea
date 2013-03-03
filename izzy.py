from __future__ import division
from ea import float_gtype
from ea import adult_selection
from ea import parent_selection
from ea import reproduction
from ea import main
from ea.ea_globals import *
import pylab
import sys
import copy
import multiprocessing as mp

def spiketrain(a, b, c, d, k,):
    '''Compute a spike train according to the Izhikevich model'''
    tau = 10
    thresh = 35
    steps = 1000
    ext_input = [10 for i in xrange(steps)]

    v = -60
    u = 0

    train = []
    for i in xrange(steps):
        train += [v]
        if v >= thresh:
            v = c
            u = u + d
        dv = 1/tau * (k * v**2 + 5*v + 140 - u + ext_input[i])
        du = a/tau * (b*v - u)
        v += dv
        u += du
    return train

def spiketrain_list(params):
    '''Take a, b, c, d and k as a list and compute the corresponding spike train'''
    return spiketrain(params[0], params[1], params[2], params[3], params[4])

def detect_spikes(spike_train):
    '''Detect spikes in a spike train using a sliding window of size k'''
    thresh = 0
    k = 5
    spikes = []
    for i in xrange(len(spike_train) - k + 1):
        window = spike_train[i:i+k]
        if window[k//2] == max(window) and window[k//2] > thresh:
            spikes += [i + k//2]
    return spikes

def dist_spike_time(train1, train2):
    '''Compute distance between two spike trains using the spike time distance metric'''
    spikes1 = detect_spikes(train1)
    spikes2 = detect_spikes(train2)

    m = min(len(spikes1), len(spikes2))
    n = max(len(spikes1), len(spikes2))

    p = 2

    dist = 0
    for i in xrange(m):
        dist += abs(spikes1[i] - spikes2[i])**p
    dist = dist ** (1/p)
    
    penalty = (n-m)*len(train1)
    penalty = penalty / max(2*m, 1)
    dist = (1/n) * (dist + penalty)

    return dist

def dist_spike_interval(train1, train2):
    '''Compute distance between two spike trains using the spike interval distance metric'''
    spikes1 = detect_spikes(train1)
    spikes2 = detect_spikes(train2)
    
    n = max(len(spikes1), len(spikes2))
    m = min(len(spikes1), len(spikes2))
    p = 2
    
    dist = sum(abs((spikes1[i] - spikes1[i-1])-(spikes2[i] - spikes2[i-1]))**p for i in xrange(1,m)) ** (1/p)
    
    penalty = (n - m) * len(train1) / max(2*m, 1)    
    dist = 1/max(m-1, 1) * (dist + penalty)

    return dist

def dist_waveform(train1, train2):
    '''Compute distance between two spike trains using the waveform distance metric'''
    m = len(train1)
    p = 2

    dist = 1/m * sum(abs(train1[i] - train2[i]) ** p for i in xrange(m)) ** (1/p)
    return dist

def fitness_test(population, target, dist):
    '''Compute fitnesses based on distance to the target spike train'''
    tested = population
    for ind in tested:
        if ind.fitness != None:
            continue
        distance = dist(ind.ptype, target)
        if distance != 0:
            ind.fitness = 1 / distance
        else:
            ind.fitness = float('Inf')
    return tested

def fitness_test_mp(population, target, dist):
    '''Compute fitnesses based on distance to the target spike train'''
    pool = mp.Pool(mp.cpu_count())
    tested = population
    indices = []
    workers = []
    for i, ind in enumerate(population):
        if ind.fitness == None:
            indices += [i]
            workers += [pool.apply_async(dist, [ind.ptype, target])]
    for i, worker in enumerate(workers):
        distance = worker.get()
        if distance != 0:
            population[indices[i]].fitness = 1 / distance
        else:
            population[indices[i]].fitness = float('Inf')
    pool.close()
    pool.join()
    return tested
        

def gen_fitness(target):
    '''Generate a fitness function interactively'''
    while True:
        method = raw_input("Input distance metric (time/interval/waveform):\n")
        if method == 'time':
            return (lambda population: fitness_test_mp(population, target, dist_spike_time))
        elif method == 'interval':
            return (lambda population: fitness_test_mp(population, target, dist_spike_interval))
        elif method == 'waveform':
            return (lambda population: fitness_test_mp(population, target, dist_waveform))
        else:
            print "Unrecognized method: " + method

def develop(population):
    '''Development function, generates spike train for each individual'''
    developed = population    
    for ind in developed:
        if ind.ptype != None:
            continue
        ind.ptype = spiketrain_list(ind.gtype)
    return developed

def develop_mp(population):
    '''Development function that makes use of multiprocessing'''
    developed = population
    workers = []
    indices = []
    pool = mp.Pool(mp.cpu_count())
    for i, ind in enumerate(developed):
        if ind.ptype != None:
            continue
        indices += [i]
        workers += [pool.apply_async(spiketrain_list, [ind.gtype])]
    for i, worker in enumerate(workers):
        population[indices[i]].ptype = worker.get()
    pool.close()
    pool.join()
    return developed

def visualize(generation_list, target):
    '''Generate pretty pictures using pylab'''
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
    pylab.title("Fitness plot - Izzy")
    pylab.xlabel("Generation")
    pylab.ylabel("Fitness")
    pylab.legend(loc="upper left")
    pylab.savefig("izzy_fitness.png")

    best_index = best.index(max(best))
    best_individual = most_fit(generation_list[best_index])
    best_spiketrain = best_individual.ptype

    print best_individual.gtype

    pylab.figure(2)
    pylab.plot(range(len(best_spiketrain)), best_spiketrain, color='r', label='Best solution')
    pylab.plot(range(len(target)), target, color='blue', label='Target')
    pylab.title("Spiketrain plot")
    pylab.xlabel("Time - t")
    pylab.ylabel("Activation level - v")
    pylab.legend(loc="upper right")
    pylab.savefig("izzy_spiketrains.png")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Error: No filename given"
        sys.exit()

    target_file = open(sys.argv[1])
    target_spiketrain = [float(num) for num in target_file.read().split()]

    ranges = [(0.001, 0.2), (0.01, 0.3), (-80.0, -30.0), (0.1, 10.0), (0.01, 1.0)]

    popsize = int(raw_input("Input population size:\n"))
    fitness_tester = gen_fitness(target_spiketrain)
    adult_selector, litter_size = adult_selection.gen_adult_selection(popsize)
    parent_selector = parent_selection.gen_parent_selection(litter_size)
    
    mutate = float_gtype.gen_mutate(ranges)
    crossover = float_gtype.gen_crossover()
    reproducer = reproduction.gen_reproduction(mutate, crossover)

    generations = int(raw_input("Input max number of generations:\n"))
    fitness_goal = float(raw_input("Input fitness goal, 0 for none:\n"))

    initial = [individual(gtype=float_gtype.generate(ranges), age=0) for i in xrange(popsize)]
    generation_list = main.evolutionary_algorithm(initial, develop_mp, fitness_tester, adult_selector, parent_selector, reproducer, generations, fitness_goal)

    visualize(generation_list, target_spiketrain)
