from nose.tools import assert_equals
from sklearn import datasets

from cog_classification.steels.steels_agent import SteelsAgent
from cog_classification.core.environment import Environment


class DummyFitness:

    def __init__(self):
        self.success = 0
        self.all = 0

    def get_measure(self):
        if self.all == 0:
            return 0
        else:
            return float(self.success) / self.all

    def update(self, value):
        self.all += 1
        self.success += value


class TestAgent:
    """
    Functions tested in TestAgent:
    - classify

    Functions not tested:
    - __init__
    - add_sample
    - decrease_weight_word_category
    - forget
    - increase_weights_sample_category
    - increase_weight_word_category
    - learn
    - update_fitness_measure
    - decrease_weights_for_other_categories
    - decrease_weights_for_other_words
    - get_category_class
    - get_id
    - get_fitness_measure
    - get_words
    - set_fitness
    """

    def __init__(self):
        self.agent = None

        irises = datasets.load_iris()
        self.environment = Environment(irises.data, irises.target)

    def add(self, sample_index, category=None, environment=None):
        environment = environment or self.environment
        self.agent.add_sample(sample_index, environment, category)

    def classify(self, sample=None):
        if sample is None:
            sample = self.environment.get_random_sample()
        return self.agent.predict(sample)

    def setup(self):
        self.agent = SteelsAgent()

    def test_classify(self):
        sample_index, _, _ = self.environment.get_random_sample()
        sample = self.environment.get_sample(sample_index)

        # Classify with no samples returns None
        assert_equals(self.classify(sample), None)

        # Classify with one sample returns this sample category
        self.add(1, 2)
        assert_equals(self.classify(sample), 2)

        # Classify before fitting (learning) returns None
        self.add(51, 1)
        assert_equals(self.classify(sample), None)

        # Classify after fitting (learning) doesn't return None
        self.agent.learn()
        assert self.classify(sample) is not None

    def test_learning_cycle(self):
        self.add(1, 1)
        self.add(51, 2)
        self.add(101, 3)
        self.agent.learn()
        for _ in range(10):
            assert self.classify() is not None

    def test_single_classification_game_iterations(self):
        agent = self.agent
        env = self.environment

        agent.set_fitness("DF", DummyFitness())
        for _ in range(100):
            agent.learn()
            sample_index = env.get_random_sample_index()
            sample = env.get_sample(sample_index)
            category = agent.predict(sample)
            if category is None:
                self.add(sample_index)
                value = 0
            elif env.get_class(sample_index) == agent.get_category_class(category):
                agent.increase_weights_sample_category(sample_index, env, category)
                value = 1
            elif agent.get_fitness_measure("DF") > 0.95:
                agent.increase_weights_sample_category(sample_index, env, category)
                value = 0
            else:
                self.add(sample_index)
                value = 0

            self.agent.update_fitness_measure("DF", value)
            self.agent.forget()
