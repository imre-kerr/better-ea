import random

class binary_genotype:
    bits = [] # bits: list of 0s and 1s
    def __init__(self, length):
        self.bits = [0] * length
    
    def randomize(self, length):
        for i in xrange(length):
            self.bits[i] = random.randint(0, 1)
        
def crossover(gene1, gene2, points, chance):
    
        
def gen_crossover():
    points = int(raw_input("Input no. of crossover points: "))
    chance = int(raw_input("Input per-point crossover chance: "))
    return (lambda gene1, gene2: crossover(gene1, gene2, points, chance))