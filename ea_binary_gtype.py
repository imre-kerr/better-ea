import random

def generate(length):
    return [random.randint() for i in xrange(length)]
        
def crossover(gene1, gene2, num_points):
    points = random.sample(xrange(1, len(gene1) - 1), num_points) + [len(gene1)]
    crossed_bits = gene1.copy()
    for start in xrange(0, len(points)-1, 2):
        end = start + 1
        for i in xrange(points[start], points[end]):
            crossed_bits[i] = gene2[i]
    return crossed_bits
        
def gen_crossover():
    points = int(raw_input("Input no. of crossover points: "))
    return (lambda gene1, gene2: crossover(gene1, gene2, points))
    
def bitwise_mutate(gene, chance):
    mutated_bits = gene.copy()
    for i in xrange(len(mutated_bits)):
        if random.random() <= chance:
            mutated_bits[i] = mutated_bits[i] ^ 1
    return mutated_bits
    
def genewise_mutate(gene, chance):
    mutated_bits = gene.copy()
    if random.random() <= chance:
        bit = random.randint(0, len(mutated_bits) - 1)
        mutated_bits[bit] = mutated_bits[bit] ^ 1
    return mutated_bits
    
def gen_mutate():
    while True:
        if method == 'bitwise':
            chance = float(raw_input("Input per-bit mutation rate: "))
            return (lambda gene: bitwise_mutate(gene, chance))
        elif method == 'genewise':
            chance = float(raw_input("Input per-gene mutation rate: "))
            return (lambda gene: genewise_mutate(gene, chance))
        else:
            print "Method not recognized: " + method
            method = raw_input("Input mutation type (bitwise/genewise): ")
