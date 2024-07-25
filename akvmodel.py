from typing import Callable

import numpy as np


class AKV:
    """AKV is a class that instantiates AKV models.

    Args:
        belief_state (list[list[float]]): The initial belief state as a list.
        influence_graph (list[list[float]]): The influence graph as a adjacency \
            list.
        update_function(Callable[[list[list[float]], list[list[float]]], list[list[float]]): \
            A function the gets a belief_state and an influence_graph and returns a \
            new belief_state.

    Attributes:
        belief_state (list[list[float]]): Current belief state. It's a list of \
            lists, each list whitin is a belief array corresponding to the i-th \
            outcome in the domain.
        influence_graph (list[list[float]]): Adjacency list for the influence graph.
        a (int): Number of agents.
        k (int): Size of the domain of independent outcomes for a proposition.
        states (list[list[list[float]]]): list of all belief states computed so far \
            using the update function.
    """

    def _check_sizes(self):
        """Check if the size of the belief state and the size of the nodes in the
        influence graph match.

        Raises:
            Exception: If the number of beliefs and the number of nodes in the \
                influence graph are different.
            Exception: If the influence graph is not a square matrix.
        """
        if self.belief_state.shape[1] != self.influence_graph.shape[0]:
            raise Exception(
                "Number of agents in belief_state and in the influence graph are different."
            )

        if self.influence_graph.shape[0] != self.influence_graph.shape[1]:
            raise Exception("Influcence graph must be a square matrix")

    def _check_influence_graph(self):
        """Check the weights in the influence graph.

        Raises:
            Exception: If any weight is not between 0 and 1
        """
        if np.any(self.influence_graph < 0) or np.any(self.influence_graph > 1):
            raise Exception("Influence must be between 0 and 1")

    def _check_belief_state(self):
        """Check the belief values in the belief state.

        Raises:
            Exception: If any belief value is not between 0 and 1.
        """
        if np.any(self.belief_state < 0) or np.any(self.belief_state > 1):
            raise Exception("Belief values must be between 0 and 1")

    def __init__(
        self,
        belief_state: list[list[float]],
        influence_graph: list[list[float]],
        update_function: Callable[
            [list[list[float]], list[list[float]]], list[list[float]]
        ],
    ):
        self.belief_state = np.array(belief_state)
        self.influence_graph = np.array(influence_graph)

        self._check_sizes()

        self.a = self.belief_state.shape[1]
        self.k = self.belief_state.shape[0]

        self._check_influence_graph()
        self._check_belief_state()

        self.states = np.array([belief_state])
        self.update_function = update_function

    @property
    def number_of_agents(self) -> int:
        """Get the number of agents.

        Returns:
            int: Number of agents.
        """
        return self.a

    @property
    def domain_size(self) -> int:
        """Get the domain size, i.e. the number of belief arrays within a belief state.

        The domain represents a set of independent propositions.

        Returns:
            int: The number of independent propositions.
        """
        return self.k

    def update(self) -> list[list[float]]:
        """Update the model one, updates the current belief state and add the new belief
        state to the history of states.

        Returns:
            list[list[float]]: New belief state.
        """
        new_belief_state = self.update_function(self.belief_state, self.influence_graph)
        self.belief_state = new_belief_state
        self.states = np.vstack((self.states, [self.belief_state]))
        return self.belief_state

    def get_polarization(
        self, k: int = 201, K: float = 1000, alpha: float = 1.6
    ) -> list[list[float]]:
        """Get Esteban-Ray polarization for all states in the history.

        Args:
            k (int, optional): Number of bins. Defaults to 201.
            K (float, optional): Hyperparameter K of the Esteban-Ray measure. Defaults \
                to 1000.
            alpha (float, optional): Hyperparameter $\alpha$ of the Esteban-Ray \
                measure. Defaults to 1.6.

        Returns:
            list[float]: list of polarization values.
        """

        def polarization(belief_array):
            pi, bin_edges = np.histogram(
                belief_array, bins=k, range=(0, 1), density=False
            )
            y = [bin_edges[i] + (1 / k) / 2 for i in range(k)]
            pi = pi / np.sum(pi)

            return K * np.sum(
                np.sum(
                    np.power(pi[i], 1 + alpha) * pi[j] * np.abs(y[i] - y[j])
                    for j in range(k)
                )
                for i in range(k)
            )

        return [
            [polarization(belief_state[i]) for belief_state in self.states]
            for i in range(self.domain_size)
        ]


class InfluenceGraphs:
    """Catalog of Influence Graphs in the literature. All functions are static."""

    @staticmethod
    def clique(num_agents: int, influence: float = 1) -> list[list[float]]:
        """Creates a clique influence graph.
        
        The clique influence graph $\mathcal{I}^{clique}$ represents an idealized
        totally connected social network.

        Args:
            num_agents (int): Number of agents.
            influence (float, optional): Influence that every agent has on each \
                other. Defaults to 1.

        Returns:
            list[list[float]]: Adjacency matrix for the influence graph.
        """

        def I(i: int, j: int) -> float:
            n = num_agents
            if i == j:
                return 1
            else:
                return influence

        return [[I(i, j) for j in range(num_agents)] for i in range(num_agents)]

    @staticmethod
    def circular(num_agents: int, influence: float = 0.5) -> list[list[float]]:
        """Creates a circular influence graph.
        
        The circular influence graph $\mathcal{I}^{clique}$ represents a social network
        in which agents can be organized in a circle in such a way each agent is only
        influenced by its predecessor and only influences its successor.

        Args:
            num_agents (int): Number of agents.
            influence (float, optional): Influence that an agent has on the next one. \
                Defaults to 0.5.

        Returns:
            list[list[float]]: Adjacency matrix for the influence graph.
        """

        def I(i: int, j: int) -> float:
            n = num_agents
            if i == j:
                return 1
            elif (i + 1) % n == j:
                return influence
            else:
                return 0

        return [[I(i, j) for j in range(num_agents)] for i in range(num_agents)]

    @staticmethod
    def faintly(
        num_agents: int, strong_influence: float = 0.5, weak_influence: float = 0.1
    ) -> list[list[float]]:
        """Creates a faintly communicating influence graph.
        
        The faintly communicating influence graph $\mathcal{I}^{faint}$ represents a
        social network divided into two groups that evolve mostly separately, with only
        faint communication between them. More precisely, agents from within the same
        group influence each other much more strongly than from different groups.

        Args:
            num_agents (int): Number of agents.
            strong_influence (float, optional): Influence between agents of the same \
                group. Defaults to 0.5.
            weak_influence (float, optional): Influence between agents from different \
                groups. Defaults to 0.1.

        Returns:
            list[list[float]]: Adjacency matrix for the influence graph.
        """

        def I(i: int, j: int) -> float:
            n = num_agents
            if i == j:
                return 1
            elif (i < np.ceil(n / 2) and j < np.ceil(n / 2)) or (
                i >= np.ceil(n / 2) and j >= np.ceil(n / 2)
            ):
                return strong_influence
            else:
                return weak_influence

        return [[I(i, j) for j in range(num_agents)] for i in range(num_agents)]

    @staticmethod
    def disconnected(num_agents: int, influence: float = 0.5) -> list[list[float]]:
        """Creates a disconnected influence graph.
        
        The disconnected influence graph $\mathcal{I}^{disc}$ represents a social
        network sharply divided into two groups in such a way that agents with the same
        group can considerably influence each other, just not all agents in the other
        group.

        Args:
            num_agents (int): Number of agents.
            influence (float, optional): Influence between agents of the same \
                group. Defaults to 0.5.

        Returns:
            list[list[float]]: Adjacency matrix for the influence graph.
        """
        return InfluenceGraphs.faintly(num_agents, influence, 0)

    @staticmethod
    def malleable_influencers(
        num_agents: int,
        influencer_1_influence: float = 0.8,
        influencer_2_influence: float = 0.4,
        influence_on_influencer_1: float = 0.1,
        influence_on_influencer_2: float = 0.1,
        other_agents_influence: float = 0.1,
    ) -> list[list[float]]:
        """Creates a malleable influencers influence graph.
        
        The malleable influencers influence graph $\mathcal{I}^{malleable}$ represents a
        social network in which two agents have a strong influence on every other agent,
        but are barely influenced by anyone else.

        Args:
            num_agents (int): Number of agents.
            influencer_1_influence (float, optional): Influence that agent 0 has on \
                other agents. Defaults to 0.8.
            influencer_2_influence (float, optional): Influence that agents n - 1 has \
                on other agents. Defaults to 0.4.
            influence_on_influencer_1 (float, optional): Influence that other agents \
                have on agent 0. Defaults to 0.1.
            influence_on_influencer_2 (float, optional): Influence that other agents \
                have on agent n - 1. Defaults to 0.1.
            other_agents_influence (float, optional): Influence that the other agents \
                have on each other. Defaults to 0.1.

        Returns:
            list[list[float]]: Adjacency matrix for the influence graph.
        """

        def I(i: int, j: int) -> float:
            n = num_agents
            if i == j:
                return 1
            elif i == 0 and j != n - 1:
                return influencer_1_influence # 0.8
            elif i == n - 1 and j != 0:
                return influencer_2_influence # 0.4
            elif j == 0:
                return influence_on_influencer_1 # 0.1
            elif j == n - 1:
                return influence_on_influencer_2 # 0.1
            else:  # if i != 0 and i != n - 1 and j != 0 and j != n -1
                return other_agents_influence # 0.1

        return [[I(i, j) for j in range(num_agents)] for i in range(num_agents)]

    @staticmethod
    def unrelenting_influencers(
        num_agents: int,
        influencer_1_influence: float = 0.6,
        influencer_2_influence: float = 0.6,
        other_agents_influence: float = 0.1,
    ) -> list[list[float]]:
        """Creates an unrelenting influencers influence graph.
        
        The unrelenting influencers influence graph $\mathcal{I}^{unrel}$ represents a
        scenario in which two agents (say, $0$ and $n - 1$) exert a significantly
        stronger influence on every other agent than those other agents have among
        themselves.

        Args:
            num_agents (int): Number of agents.
            influencer_1_influence (float, optional): Influence that agent 0 has on \
                other agents. Defaults to 0.6.
            influencer_2_influence (float, optional): Influence that agents n - 1 has \
                on other agents. Defaults to 0.6.
            other_agents_influence (float, optional): Influence that the other agents \
                have on each other. Defaults to 0.1.

        Returns:
            list[list[float]]: Adjacency matrix for the influence graph.
        """
        return InfluenceGraphs.malleable_influencers(
            num_agents,
            influencer_1_influence=influencer_1_influence,
            influencer_2_influence=influencer_2_influence,
            influence_on_influencer_1=0,
            influence_on_influencer_2=0,
            other_agents_influence=other_agents_influence,
        )


class InitialConfigurations:
    """Catalog of initial belief configurations in the literature."""

    @staticmethod
    def uniform(num_agents: int) -> list[list[float]]:
        """Creates a uniform belief configuration with domain of size 2.

        The uniform belief configuration represents a set of agents whose beliefs are as
        varied as possible, all equally spaced in the interval $[0, 1]$.

        Args:
            num_agents (int): Number of agents.

        Returns:
            list[list[float]]: Belief state for the inicial configuration.
        """

        def B(i: int) -> float:
            return i / (num_agents - 1)

        return [
            [B(i) for i in range(num_agents)],
            [1 - B(i) for i in range(num_agents)],
        ]

    @staticmethod
    def mildly(num_agents: int) -> list[list[float]]:
        """Creates a mildly polarized belief configuration with domain of size 2.

        The mildly polarized belief configuration with agents evenly split into two
        groups with moderately dissimilar inter-group belief compared to intra-groups
        beliefs

        Args:
            num_agents (int): Number of agents.

        Returns:
            list[list[float]]: Belief state for the inicial configuration.
        """

        def B(i: int) -> float:
            n = num_agents
            if i < np.ceil(n / 2):
                return (0.2 * i) / (np.ceil(n / 2)) + 0.2
            else:
                return (0.2 * (i - np.ceil(n / 2))) / (n - np.ceil(n / 2)) + 0.6

        return [
            [B(i) for i in range(num_agents)],
            [1 - B(i) for i in range(num_agents)],
        ]

    @staticmethod
    def extreme(num_agents: int) -> list[list[float]]:
        """Creates an extremely polarized belief configuration with domain of size 2.

        The extremely polarized belief configuration represents a situation in which
        half of the agents strongly believe the proposition, whereas half strongly
        disbelief it.

        Args:
            num_agents (int): Number of agents.

        Returns:
            list[list[float]]: Belief state for the inicial configuration.
        """

        def B(i: int) -> float:
            n = num_agents
            if i < np.ceil(n / 2):
                return (0.2 * i) / (np.ceil(n / 2))
            else:
                return (0.2 * (i - np.ceil(n / 2))) / (n - np.ceil(n / 2)) + 0.8

        return [
            [B(i) for i in range(num_agents)],
            [1 - B(i) for i in range(num_agents)],
        ]

    @staticmethod
    def tripolar(num_agents: int) -> list[list[float]]:
        """Creates an tripolar belief configuration with domain of size 2.

        The tripolar belief configuration with agents divided into three groups.

        Args:
            num_agents (int): Number of agents.

        Returns:
            list[list[float]]: Belief state for the inicial configuration.
        """

        def B(i: int) -> float:
            n = num_agents
            if i < np.floor(n / 3):
                return (0.2 * i) / (np.floor(n / 3))
            elif np.floor(n / 3) <= i and i < np.ceil(2 * n / 3):
                return (0.2 * (i - np.floor(n / 3))) / (
                    np.ceil(2 * n / 3) - np.floor(n / 3)
                ) + 0.4
            else:
                return (0.2 * (i - np.floor(2 * n / 3))) / (
                    n - np.ceil(2 * n / 3)
                ) + 0.8

        return [
            [B(i) for i in range(num_agents)],
            [1 - B(i) for i in range(num_agents)],
        ]


class UpdateFunctions:
    """Catalog of update functions in the literature. All functions are static."""

    @staticmethod
    def classic(
        belief_state: list[list[float]], influence_graph: list[list[float]]
    ) -> list[list[float]]:
        """Computes the classic update of a belief state given a influence graph.

        Args:
            belief_state (list[list[float]]): Belief state at time $t$.
            influence_graph (list[list[float]]): Influence graph as a adjacency matrix.

        Returns:
            list[list[float]]: Belief state at time $t + 1$.
        """

        def next_b(i, belief_array):
            a_i = [
                j for j in range(len(influence_graph[i])) if influence_graph[i][j] > 0
            ]
            return belief_array[i] + (1 / len(a_i)) * np.sum(
                influence_graph[j][i] * (belief_array[j] - belief_array[i])
                for j in range(len(a_i))
            )
        
        return [
            [next_b(i, belief_array) for i in range(len(belief_array))]
            for belief_array in belief_state
        ]

    @staticmethod
    def confirmation_bias(
        belief_state: list[list[float]], influence_graph: list[list[float]]
    ) -> list[list[float]]:
        """Computes the confirmation bias update of a belief state given a influence
        graph.

        Args:
            belief_state (list[list[float]]): Belief state at time $t$.
            influence_graph (list[list[float]]): Influence graph as a adjacency matrix.

        Returns:
            list[list[float]]: Belief state at time $t + 1$.
        """

        def next_b(i, belief_array):
            a_i = [
                j for j in range(len(influence_graph[i])) if influence_graph[i][j] > 0
            ]
            return belief_array[i] + (1 / len(a_i)) * np.sum(
                (1 - np.abs(belief_array[j] - belief_array[i]))
                * influence_graph[j][i]
                * (belief_array[j] - belief_array[i])
                for j in range(len(a_i))
            )

        return [
            [next_b(i, belief_array) for i in range(len(belief_array))]
            for belief_array in belief_state
        ]
