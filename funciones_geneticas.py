import random
from individuo_gen import Individuo
from alg_gen import tournament_size,mutation_rate,mutation_strength

def tournament_selection(population, tournament_size=3):
    # Selecciona 'tournament_size' individuos al azar y devuelve el de mayor fitness.
    selected = random.sample(population, tournament_size)
    best = max(selected, key=lambda indiv: indiv.fitness)
    return best

def crossover(parent1, parent2):
    child = Individuo()
    new_weights = []
    # Cruce uniforme: para cada peso, se elige de uno u otro padre
    for w1, w2 in zip(parent1.election, parent2.election):
        new_weights.append(w1 if random.random() < 0.5 else w2)
    # Normalizar para que la suma sea 1
    total = sum(new_weights)
    if total == 0:
        new_weights = [1/len(new_weights)] * len(new_weights)
    else:
        new_weights = [w / total for w in new_weights]
    child.election = new_weights
    return child

def mutate(indiv, mutation_rate=0.1, mutation_strength=0.05):
    new_weights = []
    for w in indiv.election:
        if random.random() < mutation_rate:
            w += random.uniform(-mutation_strength, mutation_strength)
            if w < 0:
                w = 0
        new_weights.append(w)
    total = sum(new_weights)
    if total == 0:
        new_weights = [1/len(new_weights)] * len(new_weights)
    else:
        new_weights = [w / total for w in new_weights]
    indiv.election = new_weights
    return indiv

import copy

def reproduce_population(population, elite_size=2, new_size=None):
    if new_size is None:
        new_size = len(population)
    # Ordena la población por fitness de mayor a menor
    sorted_pop = sorted(population, key=lambda indiv: indiv.fitness, reverse=True)
    new_population = []
    # Elitismo: conservar los mejores individuos sin cambios (usando una copia)
    new_population.extend([copy.deepcopy(ind) for ind in sorted_pop[:elite_size]])
    # Generar nuevos individuos hasta alcanzar el tamaño deseado
    while len(new_population) < new_size:
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate, mutation_strength)
        new_population.append(child)
    return new_population
