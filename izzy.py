from __future__ import division
from ea import float_gtype
from ea.named_tuples import *

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
    return spiketrain(params[0], params[1], params[2], params[3], params[4], params[5])

def detect_spikes(spike_train):
    '''Detect spikes in a spike train using a sliding window of size k'''
    thresh = 0
    k = 5
    spikes = []
    for i in xrange(len(spike_train) - k + 1):
        window = spike_train[i:i+k]
        if window[k/2] == max(window) and window[k/2] > thresh:
            spikes += [window[k/2]]
    return spikes

def dist_spike_time(train1, train2):
    '''Compute distance between two spike trains using the spike time distance metric'''
    spikes1 = detect_spikes(train1)
    spikes2 = detect_spikes(train2)
    
    n = min(len(spikes1), len(spikes2))
    p = 2
    
    dist = sum(abs(spikes1[i] - spikes2[i])**p for i in xrange(n)) ** (1/p)
    
    # Note that m and n are reversed in relation to their names in izzy-evo.pdf
    m = max(len(train1), len(train2))
    penalty = (m - n) * len(train1) / (2 * n)
    dist = 1/n * (dist + penalty)

    return dist + penalty

def dist_spike_interval(train1, train2):
    '''Compute distance between two spike trains using the spike interval distance metric'''
    spikes1 = detect_spikes(train1)
    spikes2 = detect_spikes(train2)
    
    n = min(len(spikes1), len(spikes2))
    p = 2
    
    dist = sum(abs((spikes1[i] - spikes1[i-1])-(spikes2[i] - spikes2[i-1]))**p for i in xrange(1,n)) ** (1/p)
    
    # Note that m and n are reversed in relation to their names in izzy-evo.pdf
    m = max(len(train1), len(train2))
    penalty = (m - n) * len(train1) / (2 * n)    
    dist = 1/(n-1) * (dist + penalty)

    return dist

def dist_waveform(train1, train2):
    '''Compute distance between two spike trains using the waveform distance metric'''
    m = len(train1)
    p = 2

    dist = 1/m * sum(abs(train1[i] - train2[i]) ** p for i in xrange(m)) ** (1/p)
    return dist

def fitness_test(population, target , dist):
    '''Compute fitnesses based on distance to the target spike train'''
    tested = []
    for ind in population:
        fitness = 1 / dist(ind.ptype, target)
        tested += [gpfa_t(gtype=ind.gtype, ptype=ind.ptype, fitness=fitness, age=ind.age)]
    return tested

def gen_fitness(target):
    '''Generate a fitness function interactively'''
    while True:
        method = raw_input("Input distance metric (time/interval/waveform):\n")
        if method == 'time':
            return (lambda population: fitness_test(population, target, dist_spike_time))
        elif method == 'interval':
            return (lambda population: fitness_test(population, target, dist_spike_interval))
        elif method == 'waveform':
            return (lambda population: fitness_test(population, target, dist_waveform))
        else:
            print "Unrecognized method: " + method

def develop(population):
    '''Development function, generates spike train for each individual'''
    developed = []
    for ind in population:
        developed += [gpa_t(gtype=ind.gtype, ptype=spiketrain_list(ind.gtype), age=ind.age)]
    return developed
    
if __name__ == '__main__':
    popsize = int(raw_input("Input population size:\n"))
    target_file = # TODO: Read from file and whatnot
    fitness_tester = gen_fitness(target_file)
    adult_selector, litter_size = adult_selection.gen_adult_selection(popsize)
    parent_selector = parent_selection.gen_parent_selection(litter_size)
    
    mutate = float_gtype.gen_mutate()
    crossover = float_gtype.gen_crossover()
    reproducer = reproduction.gen_reproduction(mutate, crossover)

    generations = int(raw_input("Input max number of generations:\n"))
    fitness_goal = float(raw_input("Input fitness goal, 0 for none:\n"))

    ranges = [(0.001, 0.2), (0.01, 0.3), (-80, -30), (0.1, 10), (0.01, 1)]
    initial = [ga_t(gtype=float_gtype.generate(ranges), age=0)]
    generation_list = main.evolutionary_algorithm(initial, develop, fitness_tester, adult_selector, parent_selector, reproducer, generations, fitness_goal)

