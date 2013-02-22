def reproduction(parent_list, mutate, crossover):
    '''Create a new population of gtypes by crossing and mutating each pair of input gtypes'''
    kids = []
    for mom, dad in parent_list:
        kid = crossover(mom, dad)
        kid = mutate(kid)
        kids += [(kid, 0)]
    return kids

def gen_reproducton(mutate, crossover):
    '''Generate a reproduction function'''
    return (lambda parent_list: reproduction(parent_list, mutate_crossover))
