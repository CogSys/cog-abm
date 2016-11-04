from sklearn import datasets
from nose.tools import assert_equal

from cog_classification.steels_universal.guessing_game import GuessingGame
from cog_classification.steels.discrimination_game import DiscriminationGame
from cog_classification.steels.steels_agent import SteelsClassificationAgent
from cog_classification.core.behavior_switcher import BehaviorSwitcher
from cog_classification.core import *
from cog_classification.tools.topology_generator import generate_topology


class TestGuessingGame:

    def __init__(self):
        pass

    @staticmethod
    def lexicon_and_sample_storage_adequacy(age):
        assert all([category in age.sample_storage.get_categories() for category in age.lexicon.get_categories()])

    @staticmethod
    def test_guessing_game():
        agents = {}

        for _ in range(10):
            the_agent = SteelsClassificationAgent()
            the_agent.set_fitness("DG", fitness.StandardFitness())
            the_agent.set_fitness("GG", fitness.StandardFitness())
            agents[the_agent.get_id] = the_agent

        topology = generate_topology("clique", agents_names=agents.keys())

        complete_network = network.Network(agents, {"g": topology})

        iris = datasets.load_iris()
        the_environment = environment.Environment(iris.data, iris.target)

        sim = simulation.Simulation(complete_network, BehaviorSwitcher({"a": GuessingGame()}),
                                    BehaviorSwitcher({"a": the_environment}), result.StandardResult(),
                                    condition.IterationCondition(3200))

        sim.run()

    def test_lexicon_sample_storage_adequacy(self):
        game = DiscriminationGame()

        the_agent = SteelsClassificationAgent()

        iris = datasets.load_iris()
        the_environment = environment.Environment(iris.data, iris.target)

        the_agent.add_sample(1, the_environment)
        self.lexicon_and_sample_storage_adequacy(the_agent)

        the_agent.forget()
        self.lexicon_and_sample_storage_adequacy(the_agent)

        category = the_agent.predict(the_environment.get_sample(1))
        self.lexicon_and_sample_storage_adequacy(the_agent)

        word = the_agent.find_word_for_category(category)
        self.lexicon_and_sample_storage_adequacy(the_agent)

        the_agent.forget()
        self.lexicon_and_sample_storage_adequacy(the_agent)

        game.learning_after_game(the_agent, 2, the_environment, category, True)
        self.lexicon_and_sample_storage_adequacy(the_agent)

        for _ in range(1000):
            the_agent.forget()
            self.lexicon_and_sample_storage_adequacy(the_agent)

        assert_equal(0, the_agent.sample_storage.get_categories_size())
        assert_equal(0, the_agent.lexicon.get_categories_size())
