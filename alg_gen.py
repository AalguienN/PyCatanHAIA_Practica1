from Managers.GameDirector import GameDirector
import AgentsGeneticCatan2025.helpers as helpers 
from individuo_gen import Individuo as Individuo

from funciones_geneticas import *

from tqdm import tqdm

import concurrent.futures
import random
import numpy as np
import os
import argparse

# Valores por defecto
extra_name = ""

# Parámetros del algoritmo
num_indiv = 25

# Parámetros para la evolución
generations = 100
games_per_generation = 150
games_per_agent_standarized = 5 #Sólo lo uso para partidas estandarizadas (1 vs 3 neutrales)
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
        if idx == -1: continue # Individuo equiprobable
        individuos[idx].fitness += fitness[num]

def average_fitness():
    global individuos
    for idx in range(len(individuos)):
        individuos[idx].fitness /= games_per_agent_standarized

def get_random_indiv(already_selected=[]):
    global individuos
    indiv = -1
    while indiv == -1 or indiv in already_selected:
        indiv = random.randrange(0, len(individuos))
    return indiv

def get_indi(i,individuos):
    if i == -1:
        i_neutral = Individuo()
        i_neutral.uniform_election_weights()
        return i_neutral.random_agent()
    else:
        return individuos[i].random_agent()

def game(individuos, jugadores):
    agents = [get_indi(i,individuos) for i in jugadores]
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

# Realiza una serie de juegos para evaluar la población
# Sólo entre individuos reales
def prepare_games_random_individuals():        
    partidas = []
    for _ in range(games_per_generation):
        selected_inds = []
        for _ in range(4):
            idx = get_random_indiv(selected_inds)
            selected_inds.append(idx)
        partidas.append(selected_inds)
    return partidas

# Realiza una serie de juegos para evaluar la población
# Estandarizada, cada individuo se enfrenta n veces contra 3 individuos neutrales (equiprovables de ser cualquier agente)
def prepare_games_standarized():    
    partidas = []
    for indi_id in range(num_indiv):
        for _ in range(games_per_agent_standarized):
            partida = [indi_id, -1, -1, -1] #-1 indica un individuo neutral, equiprobable a ser cualquier agente
            partidas.append(partida)
    return partidas

fitness_data = []
todos_los_individuos_probabilidades = []

def main():
    global individuos
    print("Algoritmo genético\nPyCatan")
    print("Starting...")

    # Inicialización de la población
    individuos = [Individuo() for _ in range(num_indiv)]
    for indi in individuos:
        indi.random_election_weights()
        # print("Pesos iniciales:", indi.election)

    best_probs_per_generation = []  # Store the best probabilities per generation

    for gen in range(generations):
        print(f"\n=== Generación {gen} === {len(individuos)} individuos")
        print("----------------->", )
        # Reinicia el fitness de cada individuo para la generación
        for indi in individuos:
            indi.fitness = 0
        
        partidas = prepare_games_standarized()
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(handle_game, individuos, p) for p in partidas]
            
            resultados = []
            for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Generación {gen} / {generations}"):
                jugadores, fitness = f.result()
                update_fitness(jugadores, fitness)
                resultados.append((jugadores, fitness))


        
        average_fitness()

        for idx in range(num_indiv):
            print(f"Agente {idx}: {individuos[idx].fitness}")

        # Imprime el mejor fitness de la generación
        best = max(individuos, key=lambda i: i.fitness)
        print("Mejor fitness de la generación:", best.fitness)
        print("Probabilidades mejor:", best.election)

        fitness_data.append([i.fitness for i in individuos])
        best_probs_per_generation.append(best.election)  # Save best probabilities

        generacion_probabilidades = [ind.election for ind in individuos]
        todos_los_individuos_probabilidades.append(generacion_probabilidades)

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

    df_results_todas = pd.DataFrame({
        "Generacion": np.repeat(range(generations), num_indiv),
        "Individuo": np.tile(range(num_indiv), generations),
        "Probabilidades": [','.join(map(str, probs)) for gen_probs in todos_los_individuos_probabilidades for probs in gen_probs],
        "Fitness": [f for gen in fitness_data for f in gen]
    })

    folder_path = "./data"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_filename = f"./data/{extra_name}_evolucion_fitness.csv"
    df_results.to_csv(csv_filename, index=False)

    csv_filename_all = f"./data/{extra_name}_evolucion_fitness_all.csv"
    df_results_todas.to_csv(csv_filename_all, index=False)

if __name__ == "__main__":
    # Configurar argparse para recibir parámetros desde la línea de comandos
    parser = argparse.ArgumentParser(description="Algoritmo Genético - PyCatan")

    # Parámetros del algoritmo
    parser.add_argument("--extra_name", type=str, default="", help="Nombre extra para los archivos generados")
    parser.add_argument("--num_indiv", type=int, default=25, help="Número de individuos en la población")
    parser.add_argument("--generations", type=int, default=100, help="Número de generaciones")
    parser.add_argument("--games_per_generation", type=int, default=150, help="Número de juegos por generación")
    parser.add_argument("--games_per_agent_standarized", type=int, default=5, help="Número de partidas estandarizadas por agente por generación")
    parser.add_argument("--elite_size", type=int, default=2, help="Número de individuos que se mantienen sin cambios (elitismo)")
    parser.add_argument("--tournament_size", type=int, default=3, help="Tamaño del torneo para selección")
    parser.add_argument("--mutation_rate", type=float, default=0.1, help="Probabilidad de mutar cada gen")
    parser.add_argument("--mutation_strength", type=float, default=0.05, help="Magnitud de la mutación")

    # Parsear argumentos
    args = parser.parse_args()

    # Asignar valores a las variables
    extra_name = args.extra_name
    num_indiv = args.num_indiv
    generations = args.generations
    games_per_generation = args.games_per_generation
    games_per_agent_standarized = args.games_per_agent_standarized
    elite_size = args.elite_size
    tournament_size = args.tournament_size
    mutation_rate = args.mutation_rate
    mutation_strength = args.mutation_strength

    # Mostrar los valores que se están utilizando
    print(f"Ejecutando con los siguientes parámetros:")
    print(f"  extra_name: {extra_name}")
    print(f"  num_indiv: {num_indiv}")
    print(f"  generations: {generations}")
    print(f"  games_per_generation: {games_per_generation}")
    print(f"  games_per_agent_standarized: {games_per_agent_standarized}")
    print(f"  elite_size: {elite_size}")
    print(f"  tournament_size: {tournament_size}")
    print(f"  mutation_rate: {mutation_rate}")
    print(f"  mutation_strength: {mutation_strength}")
    main()
