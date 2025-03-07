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

max_games = 100

points_for_win = 10

num_indiv = 20

individuos = []

def fitness_func(game_trace:dict):
    last_round = max(game_trace["game"].keys(), key=lambda r: int(r.split("_")[-1]))
    last_turn = max(game_trace["game"][last_round].keys(), key=lambda t: int(t.split("_")[-1].lstrip("P")))
    victory_points = game_trace["game"][last_round][last_turn]["end_turn"]["victory_points"]
    
    fitness = [int(victory_points[k])-5 for k in [f"J{i}" for i in range(4)]]
    winner = int(max(victory_points, key=lambda player: int(victory_points[player]))[1])
    fitness[winner] += points_for_win

    return fitness

def update_fitness(agents_ids,fitness):
    global individuos
    for num,id in enumerate(agents_ids):
        individuos[id].fitness += fitness[num]

def get_random_indiv(already_selected=[]):
    global individuos
    indiv = -1
    while indiv == -1 or indiv in already_selected:
        indiv = random.randrange(0,len(individuos))
    return indiv

def game(individuos):
    agents = [individuos[i].random_agent() for i in range(4)]
    try:
        game_director = GameDirector(agents=agents, max_rounds=200, store_trace=False)
        game_trace = game_director.game_start(print_outcome=False)
    except Exception as e:
        print(f"Error: {e}")
    return game_trace

def main():
    global individuos
    print("Algoritmo genético\nPyCatan")
    print("Starting...")

    ind = Indiviuo()
    ind.election = [0.0 for _ in all_agents]
    ind.election[0] = 1

    individuos = [Indiviuo() for _ in range(num_indiv)]
    for indi in individuos:indi.random_election_weights(); print(indi.election)

    for _ in range(max_games):
        selected_inds = []
        for _ in range(4):
            indiv = get_random_indiv(selected_inds)
            selected_inds.append(indiv)
        
        game_trace = game(individuos)
        fitness = fitness_func(game_trace=game_trace)
        update_fitness(selected_inds, fitness)
        print([i.fitness for i in individuos])

if __name__ == "__main__":
    main()