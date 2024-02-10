from typing import List

import numpy as np


BeliefArray = List[float]
InfluenceGraph = List[List[float]]

epsilon = 0.01

class AKV:
    def check_sizes(self):
        if self.belief_array.shape[1] != self.influence_graph.shape[0]:
            raise Exception(
                "Number of agents in belief_state and in the influence graph are different."
            )

        if self.influence_graph.shape[0] != self.influence_graph.shape[1]:
            raise Exception("Influcence graph must be a square matrix")

    def check_values(self):
        if np.any(np.sum(self.belief_array, axis=0) != 1):
            raise Exception("All belief states must sum up to 1.")

        if np.any(self.influence_graph < 0) or np.any(self.influence_graph > 1):
            raise Exception("Influence must be between 0 or 1")

        if np.any(self.belief_array < 0) or np.any(self.belief_array > 1):
            raise Exception("Influence must be between 0 or 1")

    def __init__(self, belief_array, influence_graph):
        self.belief_array = np.array(belief_array)
        self.influence_graph = np.array(influence_graph)

        self.check_sizes()

        self.a = self.belief_array.shape[0]
        self.k = self.belief_array.shape[1]

        self.check_values()

        self.states = np.array([belief_array])

    @property
    def number_of_agents(self):
        return self.a

    @property
    def domain_size(self):
        return self.k

    @staticmethod
    def classic_update(belief_state_i, belief_state_j, influence):
        return belief_state_i + influence * (belief_state_j - belief_state_i)

    def overall_class_update(self):
        new_belief_array = np.array(
            [
                [
                    1
                    / self.a
                    * np.sum(
                        [
                            AKV.classic_update(
                                self.belief_array[ai, ki],
                                self.belief_array[aj, ki],
                                self.influence_graph[aj, ai],
                            )
                            for aj in range(self.a)
                        ]
                    )
                    for ki in range(self.k)
                ]
                for ai in range(self.a)
            ]
        )
        self.belief_array = new_belief_array
        self.states = np.vstack((self.states, [self.belief_array]))
        return self.belief_array

    def get_polarization(self, k=201, K=1000, alpha=1.0):
        pis = np.array(
            [
                np.histogram(self.belief_array[:, i], bins=k, range=(0, 1))
                for i in range(self.k)
            ]
        )

        def polarization(pi):
            return K * np.sum(
                [
                    np.sum([pi[i] ** (1 - alpha) * pi[j] for j in range(k)])
                    for i in range(k)
                ]
            )

        return np.array([polarization(pis[i]) for i in range(self.k)])


class InfluenceGraphs:
    @staticmethod
    def clique(num_agents: int, influence: float):
        influence_graph = np.full((num_agents, num_agents), influence)
        for i in range(num_agents):
            influence_graph[i, i] = 1
        return influence_graph

    @staticmethod
    def circular(num_agents: int, influence: float):
        inf_graph = np.zeros((num_agents, num_agents))
        for i in range(num_agents):
            inf_graph[i, i] = 1.0
            inf_graph[i, (i + 1) % num_agents] = influence
        return inf_graph

    @staticmethod
    def disconnected(num_agents: int, influence: float):
        inf_graph = np.zeros((num_agents, num_agents))
        middle = int(np.ceil(num_agents / 2))
        inf_graph[:middle, :middle] = influence
        inf_graph[middle:, middle:] = influence
        for i in range(num_agents):
            inf_graph[i, i] = 1
        return inf_graph

    @staticmethod
    def faintly(num_agents: int, weak_influence: float, strong_influence: float):
        inf_graph = np.full((num_agents, num_agents), weak_influence)
        middle = int(np.ceil(num_agents / 2))
        inf_graph[:middle, :middle] = strong_influence
        inf_graph[middle:, middle:] = strong_influence
        for i in range(num_agents):
            inf_graph[i, i] = 1
        return inf_graph

    @staticmethod
    def two_influencers_balanced(
        num_agents,
        influencers_incoming_value,
        influencers_outgoing_value,
        others_belief_value,
    ):
        inf_graph = np.full((num_agents, num_agents), others_belief_value)
        inf_graph[0, :-1] = influencers_outgoing_value
        inf_graph[-1, 1:] = influencers_outgoing_value
        inf_graph[1:, 0] = influencers_incoming_value
        inf_graph[:-1, -1] = influencers_incoming_value
        for i in range(num_agents):
            inf_graph[i, i] = 1
        return inf_graph

    @staticmethod
    def two_influencers_unbalanced(
        num_agents,
        influencers_outgoing_value_first,
        influencers_outgoing_value_second,
        influencers_incoming_value_first,
        influencers_incoming_value_second,
        others_belief_value,
    ):
        inf_graph = np.full((num_agents, num_agents), others_belief_value)
        inf_graph[0, :-1] = influencers_outgoing_value_first
        inf_graph[-1, 1:] = influencers_outgoing_value_second
        inf_graph[1:, 0] = influencers_incoming_value_first
        inf_graph[:-1, -1] = influencers_incoming_value_second
        for i in range(num_agents):
            inf_graph[i, i] = 1
        return inf_graph
    
class InitialConfigurations:
    @staticmethod
    def uniform(num_agents: int) -> BeliefArray:
        belief_array = np.array([i / (num_agents - 1) for i in range(num_agents)])
        belief_array[0] = epsilon
        belief_array[-1] = 1 - epsilon
        return belief_array

    @staticmethod
    def mildly(num_agents: int) -> BeliefArray:
        middle = np.ceil(num_agents / 2)
        return [
            0.2 + 0.2 * i / middle
            if i < middle
            else 0.6 + 0.2 * (i - middle) / (num_agents - middle)
            for i in range(num_agents)
        ]

    @staticmethod
    def extreme(num_agents: int) -> BeliefArray:
        middle = np.ceil(num_agents / 2)
        belief_array = np.array(
            [
                0.2 * i / middle
                if i < middle
                else 0.8 + 0.2 * (i - middle) / (num_agents - middle)
                for i in range(num_agents)
            ]
        )
        belief_array[0] = epsilon
        return belief_array

    @staticmethod
    def tripolar(num_agents: int) -> BeliefArray:
        beliefs = [0.0] * num_agents
        first_third = num_agents // 3
        middle_third = np.ceil(num_agents * 2 / 3) - first_third
        last_third = num_agents - middle_third - first_third
        offset = 0
        for i, segment in enumerate((first_third, middle_third, last_third)):
            for j in range(int(segment)):
                beliefs[int(j + offset)] = 0.2 * j / segment + (0.4 * i)
            offset += segment
        beliefs[0] = epsilon
        return np.array(beliefs)