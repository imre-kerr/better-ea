def gen_mix(new, prev):
    '''Create the next generation by mixing children and adults, add 1 to adults' age'''
    return new + [(individual[0], individual[3] + 1) for individual in prev]
    
def done(pop, goal):
    '''Check if the highest fitness in the population is >= the fitness goal'''
    return max([ind[2] for ind in pop]) >= goal

def evolutionary_algorithm(initial, development, fitness_test, 
                           adult_selection, parent_selection, 
                           reproduction, generations, fitness_goal):
    '''Main EA loop. 
    
    Returns a list of all generations, each a list of (gtype, ptype, fitness) touples'''
    generation_list = [] # generation_list: [[(gtype, ptype, fitness) list] list]
    genotypes = initial # genotypes: [(gtype, age) list]
    for gen in xrange(generations):
        developed_population = develop(genotypes) # developed_population: [(gtype, ptype, age) list]
        tested_population = fitness_test(developed_population) # tested_population: [(gtype, ptype, fitness, age) list]
        culled_population = adult_selection(tested_population) # culled_population: [(gtype, ptype, age) list]            
        generation_list += culled_population
        if done(culled_population, fitness_goal):
            break
        parents = parent_selection(culled_population) # parents: [(gtype1, gtype2) list]
        offspring = reproduction(parents) # offspring: [(gtype, age) list] (age = 0)
        genotypes = gen_mix(offspring, culled_population)
    return generation_list