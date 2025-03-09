from Managers.GameDirector import GameDirector
import AgentsGeneticCatan2025.helpers as helpers 
from individuo_gen import Individuo as Individuo

from funciones_geneticas import *

from tqdm import tqdm

import concurrent.futures
import random
import numpy as np
import os



# Parámetros del algoritmo
num_indiv = 20

# Parámetros para la evolución
generations = 50
games_per_generation = 100
elite_size = 2            # Número de individuos que se mantienen sin cambios
tournament_size = 3       # Tamaño del torneo para selección
mutation_rate = 0.1       # Probabilidad de mutar cada gen
mutation_strength = 0.05  # Magnitud de la mutación

individuos = []

import pandas as pd

def fitness_func(game_trace: dict):
    if not game_trace["game"]:  # Check if the game_trace is empty
        print("Warning: Empty game trace. Assigning minimum fitness values.")
        return [0, 0, 0, 0]  # Return a neutral fitness score
    
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

def game(individuos, jugadores):
    agents = [individuos[i].random_agent() for i in jugadores]
    try:
        game_director = GameDirector(agents=agents, max_rounds=200, store_trace=False)
        game_trace = game_director.game_start(print_outcome=False)
    except Exception as e:
        print(f"Error: {e}")
        game_trace = {"game": {}}
    return game_trace

# --- Funciones de evolución (selección, cruce y mutación) ---

def handle_game(individuos,jugadores):
    game_trace = game(individuos=individuos,jugadores=jugadores)
    fitness = fitness_func(game_trace=game_trace)
    return jugadores, fitness

# --- Función principal del algoritmo genético ---

fitness_data = []

def main():
    global individuos
    print("Algoritmo genético\nPyCatan")
    print("Starting...")

    # Inicialización de la población
    individuos = [Individuo() for _ in range(num_indiv)]
    for indi in individuos:
        indi.random_election_weights()
        print("Pesos iniciales:", indi.election)

    best_probs_per_generation = []  # Store the best probabilities per generation

    for gen in range(generations):
        print(f"\n=== Generación {gen} ===")
        print("----------------->", len(individuos))
        # Reinicia el fitness de cada individuo para la generación
        for indi in individuos:
            indi.fitness = 0
        
        partidas = []
        # Realiza una serie de juegos para evaluar la población
        for _ in range(games_per_generation):
            selected_inds = []
            for _ in range(4):
                idx = get_random_indiv(selected_inds)
                selected_inds.append(idx)
            partidas.append(selected_inds)
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(handle_game, individuos, p) for p in partidas]
            
            resultados = []
            for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Generación {gen}"):
                jugadores, fitness = f.result()
                update_fitness(jugadores, fitness)
                resultados.append((jugadores, fitness))
        
        # Imprime el mejor fitness de la generación
        best = max(individuos, key=lambda i: i.fitness)
        print("Mejor fitness de la generación:", best.fitness)
        print("Probabilidades mejor:", best.election)

        fitness_data.append([i.fitness for i in individuos])
        best_probs_per_generation.append(best.election)  # Save best probabilities

        # Reproducción: se crea la nueva generación
        individuos = reproduce_population(individuos, elite_size=elite_size, new_size=num_indiv)
        print("Nueva generación creada.\n")

    best_fitness_per_generation = np.max(fitness_data, axis=1)
    avg_fitness_per_generation = np.mean(fitness_data, axis=1)
    
    # Crear DataFrame con los datos simulados
    df_results = pd.DataFrame({
        "Generacion": range(generations),
        "Fitness_Medio": avg_fitness_per_generation,
        "Fitness_Maximo": best_fitness_per_generation,
        "Mejor_Probabilidades": [",".join(map(str, probs)) for probs in best_probs_per_generation],  # Convert list to string
    })

    folder_path = "./data"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_filename = "./data/evolucion_fitness.csv"
    df_results.to_csv(csv_filename, index=False)

if __name__ == "__main__":
    main()
