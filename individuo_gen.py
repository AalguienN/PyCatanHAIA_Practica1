from alg_gen import all_agents

import random

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