from Managers.GameDirector import GameDirector
import AgentsGeneticCatan2025.helpers as helpers 
from individuo_gen import *

from Agents.RandomAgent import RandomAgent as ra
from Agents.AdrianHerasAgent import AdrianHerasAgent as aha
from Agents.AlexPastorAgent import AlexPastorAgent as ap_a
from AgentsGeneticCatan2025.AlexPelochoJaimeAgent import AlexPelochoJaimeAgent as apj_a
from AgentsGeneticCatan2025.CarlesZaidaAgent import CarlesZaidaAgent as cz_a
from AgentsGeneticCatan2025.CrabisaAgent import CrabisaAgent as c_a 
from AgentsGeneticCatan2025.EdoAgent import EdoAgent as e_a 
from AgentsGeneticCatan2025.PabloAleixAlexAgent import PabloAleixAlexAgent as pa_a
from AgentsGeneticCatan2025.SigmaAgent import SigmaAgent as s_a
from AgentsGeneticCatan2025.TristanAgent import TristanAgent as t_a

import random

all_agents = [ra, aha, ap_a, apj_a, cz_a, c_a, e_a, pa_a, s_a, t_a]

# Parámetros del algoritmo
max_games = 100  # (podrías dejar de usarlo si defines generaciones)
num_indiv = 20

# Parámetros para la evolución
generations = 50
games_per_generation = 100
elite_size = 2            # Número de individuos que se mantienen sin cambios
tournament_size = 3       # Tamaño del torneo para selección
mutation_rate = 0.1       # Probabilidad de mutar cada gen
mutation_strength = 0.05  # Magnitud de la mutación

individuos = []


def fitness_func(game_trace: dict):
    last_round = max(game_trace["game"].keys(), key=lambda r: int(r.split("_")[-1]))
    last_turn = max(game_trace["game"][last_round].keys(), key=lambda t: int(t.split("_")[-1].lstrip("P")))
    victory_points = game_trace["game"][last_round][last_turn]["end_turn"]["victory_points"]
    
    fitness = [int(victory_points[k]) - 5 for k in [f"J{i}" for i in range(4)]]
    winner = int(max(victory_points, key=lambda player: int(victory_points[player]))[1])
    fitness[winner] += 10  # puntos extra por ganar

    return fitness

def update_fitness(agents_ids, fitness):
    global individuos
    for num, idx in enumerate(agents_ids):
        individuos[idx].fitness += fitness[num]

def get_random_indiv(already_selected=[]):
    global individuos
    indiv = -1
    while indiv == -1 or indiv in already_selected:
        indiv = random.randrange(0, len(individuos))
    return indiv

def game(individuos):
    agents = [individuos[i].random_agent() for i in range(4)]
    try:
        game_director = GameDirector(agents=agents, max_rounds=200, store_trace=False)
        game_trace = game_director.game_start(print_outcome=False)
    except Exception as e:
        print(f"Error: {e}")
        game_trace = {"game": {}}
    return game_trace

# --- Funciones de evolución (selección, cruce y mutación) ---

def tournament_selection(population, tournament_size=3):
    # Selecciona 'tournament_size' individuos al azar y devuelve el de mayor fitness.
    selected = random.sample(population, tournament_size)
    best = max(selected, key=lambda indiv: indiv.fitness)
    return best

def crossover(parent1, parent2):
    child = Indiviuo()
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

def reproduce_population(population, elite_size=2, new_size=None):
    if new_size is None:
        new_size = len(population)
    # Ordena la población por fitness de mayor a menor
    sorted_pop = sorted(population, key=lambda indiv: indiv.fitness, reverse=True)
    new_population = []
    # Elitismo: conservar los mejores individuos sin cambios
    new_population.extend(sorted_pop[:elite_size])
    # Generar nuevos individuos hasta alcanzar el tamaño deseado
    while len(new_population) < new_size:
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate, mutation_strength)
        new_population.append(child)
    return new_population

# --- Función principal del algoritmo genético ---

def main():
    global individuos
    print("Algoritmo genético\nPyCatan")
    print("Starting...")

    # Inicialización de la población
    individuos = [Indiviuo() for _ in range(num_indiv)]
    for indi in individuos:
        indi.random_election_weights()
        print("Pesos iniciales:", indi.election)

    for gen in range(generations):
        print(f"\n=== Generación {gen} ===")
        print("----------------->",len(individuos))
        # Reinicia el fitness de cada individuo para la generación
        for indi in individuos:
            indi.fitness = 0
        
        # Realiza una serie de juegos para evaluar la población
        for _ in range(games_per_generation):
            selected_inds = []
            for _ in range(4):
                idx = get_random_indiv(selected_inds)
                selected_inds.append(idx)
            
            game_trace = game(individuos)
            fitness = fitness_func(game_trace=game_trace)
            update_fitness(selected_inds, fitness)
            print("Fitness:", [i.fitness for i in individuos])
        
        # Imprime el mejor fitness de la generación
        best = max(individuos, key=lambda i: i.fitness)
        print("Mejor fitness de la generación:", best.fitness)
        print("Probabilidades mejor:", best.election)
        
        # Reproducción: se crea la nueva generación
        individuos = reproduce_population(individuos, elite_size=elite_size, new_size=num_indiv)
        print("Nueva generación creada.\n")
        
if __name__ == "__main__":
    main()
