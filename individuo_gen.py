# from alg_gen import all_agents

import random

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

all_agents = [ra, aha, ap_a, apj_a, cz_a, c_a, e_a, pa_a, s_a, t_a]


class Indiviuo: 
    def __init__(self):
        self.__eleccion_prob = [0 for _ in all_agents]
        self.__fitness = 0

    @property
    def election(self):
        return self.__eleccion_prob
    
    @election.setter
    def election(self, new_probs):
        self.__eleccion_prob = new_probs

    @property
    def fitness(self):
        return self.__fitness
    
    @fitness.setter
    def fitness(self, new_fitness):
        self.__fitness = new_fitness

    def random_agent(self):
        return random.choices(all_agents, weights=self.election, k=1)[0]
    
    def random_election_weights(self):
        random_vals = [random.random() for _ in self.election]
        total = sum(random_vals)
        normalized = [val / total for val in random_vals]
        self.election = normalized
    
    def uniform_election_weights(self):
        self.election = [1/len(all_agents) for _ in all_agents]