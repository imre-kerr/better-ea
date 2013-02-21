def full_generational_replacement(population):
    '''Cull all individuals that are more than 1 generation old'''
    return [ind for ind in population if ind[3] == 0]

def overproduction(population, n):
    '''Cull all but the n most fit individuals that are no more than 1 generation old'''
    newpop = [ind for ind in population if ind[3] == 0]
    newpop.sort(key=(lambda ind: ind[2]), reverse=True)
    return [ind for ind in newpop[:n]]

def generational_mixing(population, n):
    '''Cull all but the n most fit individuals'''
    newpop = population.sorted(key=(lambda ind: ind[2]), reverse=True)
    return [ind for ind in newpop[:n]]

def gen_adult_selection(popsize):
    '''Generate an adult selection function interactively'''
    while True:
        method = raw_input("Input adult selection protocol (full/overproduction/mix): ")
        if method == 'full':
            return full_generational_replacement, popsize
        elif method == 'overproduction':
            litter_size = int(raw_input("Input litter size: "))
            return (lambda population: overproduction(population, popsize)), litter_size
        elif method == 'mix':
            litter_size = int(raw_input("Input litter size: "))
            return (lambda population: generational_mixing(population, popsize)), litter_size
        else:
            print "Unrecognized method: " + method
