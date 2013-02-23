import random

def generate(ranges):
    '''Generate a random float gtype based on ranges ((high, low) list)'''
    return [random.uniform(high, low) for high, low in ranges]

def mutate_gaussian(gtype, ranges, prob, sigma):
    '''Mutate a gtype by adding gaussian random values. Results are clipped to fit range.'''
    mutated = list(gtype)
    for i in xrange(len(mutated)):
        if random.random < prob:
            mutated[i] += random.gauss(0, sigma) * (ranges[i][1] - ranges[i][0])
            mutated[i] = max(mutated[i], ranges[i][0])
            mutated[i] = min(mutated[i], ranges[i][1])
    return mutated

def gen_mutate(ranges):
    '''Generate a mutation function interactively'''
    prob = float(raw_input("Input per-number mutation chance:\n"))
    sigma = float(raw_input("Input standard deviation for mutations:\n"))
    return (lambda gtype: mutate_gaussian(gtype, ranges, prob, sigma))

def choice_crossover(gtype1, gtype2):
    '''Cross two gtypes by randomly selecting elements from one or the other'''
    return [random.choice((gtype1[i], gtype2[i])) for i in xrange(len(gtype1))]

def weighted_average_crossover(gtype1, gtype2):
    '''Cross two gtypes by taking a randomly weighted average of each value'''
    crossed = []
    for i in xrange(len(gtype1)):
        rand = random.random()
        crossed += [gtype1[i]*rand + gtype2[i]*(1-rand)]
    return crossed

def gen_crossover():
    '''Generate a crossover function'''
    while True:
        method = raw_input("Input crossover method(choice, wavg):\n")
        if method == 'choice':
            return choice_crossover
        elif method == 'wavg':
            return weighted_average_crossover
        else:
            print "Unrecognized method: " + method

