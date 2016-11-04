from sklearn import datasets

from cog_classification.core.environment import Environment
from cog_classification.core.network import Network
from cog_classification.core.simulation import Simulation
from cog_classification.core.condition import IterationCondition
from cog_classification.core.fitness import StandardFitness
from cog_classification.core.result import StandardResult
from cog_classification.steels.discrimination_game import DiscriminationGame
from cog_classification.steels_universal.steels_agent import SteelsAgent
from cog_classification.tools.topology_generator import generate_topology
from cog_classification.core.behavior_switcher import BehaviorSwitcher


class TestSimulationOfDiscriminationGame:

    def __init__(self):
        self.simulation = None

    def test_simulation_of_discrimination_game(self):

        # Network construction.
        agents = {}

        for _ in range(10):
            agent = SteelsAgent()
            agent.set_fitness("DG", StandardFitness())
            agents[agent.get_id()] = agent

        topology = generate_topology("clique", agents_names=agents.keys())

        changes = {1: "clique"}

        network = Network(agents, {"clique": topology}, changes)

        # Interaction construction.
        interactions = BehaviorSwitcher({"DG": DiscriminationGame()}, {1: "DG"})

        # Environment construction.
        irises = datasets.load_iris()
        environment = Environment(irises.data, irises.target)
        environments = BehaviorSwitcher({"global": environment}, {1: "global"})

        # Results construction.
        result = StandardResult(100)

        # Condition construction.
        condition = IterationCondition(1000)

        # Simulation construction.
        self.simulation = Simulation(network, interactions, environments, result, condition)
