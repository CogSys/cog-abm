from cog_classification.core.agent import Agent
from cog_classification.core.condition import Condition
from cog_classification.core.network import Network
from cog_classification.core.result import StandardResult
from cog_classification.core.simulation import Simulation

from cog_classification.core.behavior_switcher import BehaviorSwitcher

from cog_classification.tools.topology_generator import generate_topology


class TestSimulation:

    def __init__(self):
        self.simulation = None

    def setup(self):
        self.simulation = None

    def test_flu_game(self):
        """
        Flu game simulates flu expanding through social network.
        """

        # Network construction.
        agents = {}

        for _ in range(100):
            agent = Agent()
            agent.set_fitness("infected", InfectedFitness())
            agents[agent.get_id()] = agent

        for agent in agents:
            agents[agent].update_fitness_measure("infected", True)
            break

        topology = generate_topology("clique", agents_names=agents.keys())

        changes = {1: "clique"}

        network = Network(agents, {"clique": topology}, changes)

        # Interaction construction.
        interactions = BehaviorSwitcher({"infection": InfectInteraction()}, {1: "infection"})

        # Environment construction.
        environment = BehaviorSwitcher({}, {})

        # Results construction.
        result = StandardResult(1)

        # Condition construction.
        condition = AllInfected()

        # Simulation construction.
        self.simulation = Simulation(network, interactions, environment, result, condition)

        simulation_result = self.simulation.run()


class InfectInteraction:

    def __init__(self):
        pass

    @staticmethod
    def interact(agents, environment):
        agents = agents.get_agents(2)
        if any([agent.get_fitness_measure("infected") for agent in agents]):
            for agent in agents:
                agent.update_fitness_measure("infected", True)


class InfectedFitness:

    def __init__(self):
        self.infected = False

    def update(self, value):
        self.infected = value

    def get_measure(self):
        return self.infected


class AllInfected(Condition):

    def end(self, agents, interactions, environment, result, end_condition, iteration):
        return all([agent.get_fitness_measure("infected") for agent in agents.get_all_agents()])

