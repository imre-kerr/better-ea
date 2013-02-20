def gen_parent_selection(litter_size):
    '''Generate a parent selection function interactively'''
    while True:
        method = raw_input("Input parent selection mechanism (uniform/proportionate/sigma/tournament): ")
        if method == 'uniform':
            return (lambda population: stochastic_uniform(population, litter_size))
        elif method == 'proportionate':
            return (lambda population: fitness_proportionate(population, litter_size))
        elif method == 'sigma':
            return (lambda population: sigma_scaling(population, litter_size))
        elif method == 'tournament':
            tournament_size = int(raw_input("Input tournament size: "))
            return (lambda population: tournament(population, litter_size, tournament_size))
        else:
            print "Unrecognized method: " + method
