from __future__ import division
from ea import adult_selection
from ea import parent_selection
from ea import reproduction
from ea import main
from ea import binary_gtype

def war(p1_orig, p2_orig, reployment_factor, loss_factor):
    '''Fight a single war and return score for each side'''
    p1 = list(p1_orig)
    p2 = list(p2_orig)
    strength1 = 1
    strength2 = 1
    reploy1 = 0
    reploy2 = 0
    score = 0
    for i in xrange(len(p1)):
        battle = cmp(strength1*(p1[i] + reploy1), strength2*(p2[i] + reploy2))
        score += battle
        if battle < 0:
            if strength1 > loss_factor:
                strength1 -= loss_factor
            else:
                strength1 = 0
            if i < len(p1) - 1:
                reploy2 += reployment_factor * (p2[i] - p1[i]) / (len(p1) - i - 1)
        elif battle > 0:
            if strength2 > loss_factor:
                strength2 -= loss_factor
            else:
                strength2 = 0
            if i < len(p1) - 1:
                reploy1 += reployment_factor * (p1[i] - p2[i]) / (len(p1) - i - 1)
    return (cmp(score, 0) + 1, cmp(0, score) + 1)

def fitness_test(population, reployment_factor, loss_factor):
    '''Blotto fitness test, a.k.a. the great war'''
    warscores = [[0] for i in xrange(len(population))]
    for i in xrange(len(population)):
        for j in xrange(1+1, len(population)):
            score1, score2 = war(population[i][1], population[j][1], reployment_factor, loss_factor)
            warscores[i] += [score1]
            warscores[j] += [score2]
    return [(ind[0], ind[1], warscores[i], ind[2]) for i, ind in enumerate(population)]
            

def develop(population):
    '''Development function for blotto. 
    Interpret groups of four bits as numbers, then normalize them so they sum to 1.0'''
    developed = []
    for ind in population:
        intlist = []
        for i in xrange(0, len(ind[0]), 4):
            intlist += [ind[0][i] * 8 + ind[0][i+1] * 4 + ind[0][i+2] * 2 + ind[0][i+3]]
        floatlist = [x / sum(intlist) for x in intlist]
        developed += [(ind[0], floatlist, ind[1])]
    return developed


def visualize(generation_list):
    '''Generate visualizations using matplotlib'''
    return None

if __name__=='__main__':
    battles = int(raw_input("Input number of battles:\n"))
    popsize = int(raw_input("Input population size:\n"))
    reployment_factor = float(raw_input("Input reployment factor:\n"))
    loss_factor = float(raw_input("Input loss factor:\n"))
    adult_selection, litter_size = adult_selection.gen_adult_selection(popsize)
    parent_selection = parent_selection.gen_parent_selection(litter_size)

    mutate = binary_gtype.gen_mutate()
    crossover = binary_gtype.gen_crossover()
    reproduction = reproduction.gen_reproduction(mutate, crossover)

    generations = int(input("Input max number of generations:\n"))
    fitness_goal = 0

    initial = [(binary_gtype.generate(4*battles), 0) for i in xrange(popsize)]
    dec_fitness_test = lambda population: fitness_test(population, reployment_factor, loss_factor)
    generation_list = main.evolutionary_algorithm(initial, develop, dec_fitness_test, adult_selection, parent_selection, reproduction, generations, fitness_goal)

    visualize(generation_list)