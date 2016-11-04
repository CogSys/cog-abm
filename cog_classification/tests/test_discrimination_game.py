import random

from sklearn import datasets

from cog_classification.steels_universal.steels_agent import SteelsAgent
from cog_classification.steels.discrimination_game import DiscriminationGame
from cog_classification.core.environment import Environment
from cog_classification.tests.test_agent import DummyFitness


class DummyNetwork:

    def __init__(self, agents):
        self.agents = agents

    def get_agent(self):
        return random.choice(self.agents)

class TestDiscriminationGame:
    """
    Functions tested in TestDiscriminationGame:
    - interact

    Functions not tested:
    - __init__
    - learning_after_game
    - play
    - sample_from_other_class
    """

    def __init__(self):
        self.agents = None

        digits = datasets.load_digits()
        self.environment = Environment(digits.data, digits.target)

        self.game = DiscriminationGame()

    def setup(self):
        agents = []
        for _ in range(10):
            agent = SteelsAgent()
            agent.set_fitness("DG", DummyFitness())
            agents.append(agent)
        self.agents = DummyNetwork(agents)

    def test_interact_long_run(self):
        for _ in range(100):
            self.game.interact(self.agents, self.environment)
