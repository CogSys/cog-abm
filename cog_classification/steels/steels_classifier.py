import random

from sklearn.utils.validation import NotFittedError
from sklearn import cross_validation

from cog_classification.core.environment import Environment
from cog_classification.core.fitness import CurrentFitness
from cog_classification.core.network import Network
from cog_classification.core.simulation import Simulation
from cog_classification.core.condition import IterationCondition
from steels_classifier_results import SteelsClassifierResults
from cog_classification.steels.guessing_game import GuessingGame
from cog_classification.steels.steels_agent import SteelsClassificationAgent
from cog_classification.tools.topology_generator import generate_topology
from cog_classification.core.behavior_switcher import BehaviorSwitcher


class SteelsClassifier:
    """
    Classifier founded on Steels and Belpaeme multi-agent network and interactions concept.

    :param classifiers: classifiers that will be used with agents creation.
    :type classifiers: list of classifiers.
    :param string role_model: the way of assign agents to roles. Described in GuessingGame.
    :param string topology: the name of topology used in classifier.
    :param integer iteration_number: the number of iteration.
    """

    def __init__(self, classifiers=None, role_model="RANDOM", topology="clique", iteration_number=1000,
                 alpha=0.99, good_agent_measure=0.95):
        self.classifiers = classifiers
        self.alpha = alpha
        self.role_model = role_model
        self.good_agent_measure = good_agent_measure
        self.simulation = None
        self.topology = topology
        self.result = None
        self.iteration_number = iteration_number
        self.condition = IterationCondition(self.iteration_number)
        self.interactions = BehaviorSwitcher(GuessingGame(good_agent_measure=self.good_agent_measure,
                                                          role_model=self.role_model))

    def clone(self):
        return type(self)(classifiers=self.classifiers,
                          role_model=self.role_model,
                          topology=self.topology,
                          iteration_number=self.iteration_number,
                          alpha=self.alpha,
                          good_agent_measure=self.good_agent_measure)

    def get_params(self, deep):
        return {"classifiers": self.classifiers,
                "role_model": self.role_model,
                "topology": self.topology,
                "iteration_number": self.iteration_number,
                "alpha": self.alpha,
                "good_agent_measure": self.good_agent_measure}

    def fit(self, x, y):
        """
        Fit the steels classifier according to the given training data.

        :param list x: samples.
        :param list y: samples' classes.
        """

        environment = Environment(x, y)

        agents = {}

        if self.classifiers is None:
            for _ in range(15):
                agent = SteelsClassificationAgent(alpha=self.alpha)
                agents[agent.id] = agent
        else:
            for classifier in self.classifiers:
                agent = SteelsClassificationAgent(classifier=classifier, alpha=self.alpha)
                agents[agent.id] = agent

        for agent in agents.values():
            agent.set_fitness("DG", CurrentFitness())
            agent.set_fitness("GG", CurrentFitness())

        network = Network(agents, {1: generate_topology(self.topology, agents_names=agents.keys())})

        self.simulation = Simulation(network, self.interactions, BehaviorSwitcher(environment),
                                     SteelsClassifierResults(), self.condition)

        self.result = self.simulation.run()

    def predict(self, samples):
        """
        :param list samples: the samples which classes are predicted.

        :raise: **NotFittedError** - if no data have been fitted yet.

        :return: the predicted classes of sample.
        :rtype: list
        """
        if self.result is not None:
            return self.result.predict(samples)
        else:
            raise NotFittedError


class SteelsClassifierExtended(SteelsClassifier):
    """
    Classifier founded on Steels and Belpaeme multi-agent network and interactions concept.

    This classifier extends standard classifier on data access options.
    """

    @staticmethod
    def accuracy(classifier, x, y):
        """
        Measure accuracy of classifier on given samples and classes.

        :param classifier: tested classifier.
        :type classifier: classifier
        :param x: samples
        :type x: iterable of samples
        :param y: classes
        :type y: iterable of classes

        :return: percentage of correct classifications.
        :rtype: float
        """
        predicted_y = classifier.predict(x)
        return float(len([i for i in range(len(y)) if y[i] == predicted_y[i]])) / len(y)

    def get_results(self, samples, classes):
        """
        :param samples: samples
        :type samples: list of samples
        :param classes: classes
        :type classes: list of classes

        :return: statistics of steels classifier
        :rtype: dictionary
        """

        # Shuffling of given data.
        data = zip(samples, classes)
        random.shuffle(data)
        samples, classes = zip(*data)
        samples = list(samples)
        classes = list(classes)

        border = len(samples) * 2 / 3

        self.fit(samples[:border], classes[:border])
        agents = self.result.results['agents']

        x = {"agents": [{"id": agent.id,
                         "lexicon_words": agent.lexicon.dictionary,
                         "lexicon_categories": agent.lexicon.categories,
                         "sample_categories": agent.sample_storage.categories,
                         "sample_classes": agent.sample_storage.classes,
                         "CS": agent.get_fitness_measure("GG"),
                         "DS": agent.get_fitness_measure("DG")
                         }
                        for agent in agents],
             "accuracy": self.accuracy(self, samples[border:], classes[border:])}

        environments = {}
        number = 0
        classes = []

        for agent in x["agents"]:
            for category in agent["sample_categories"]:
                new_sample_category = {}
                for environment in agent["sample_categories"][category]:
                    if environment not in environments:
                        environments[environment] = number
                        number += 1
                    new_sample_category[environments[environment]] = agent["sample_categories"][category][environment]
                agent["sample_categories"][category] = new_sample_category
            for category in agent["sample_classes"]:
                sample_class = agent["sample_classes"][category]
                if sample_class not in classes:
                    classes.append(sample_class)
                agent["sample_classes"][category] = classes.index(sample_class)

        return x

    def get_statistics(self, samples, classes):
        """
        :param samples: samples
        :type samples: list of samples
        :param classes: classes
        :type classes: list of classes

        :return: statistics of steels classifier
        :rtype: dictionary

        2/3 of samples and classes will be used to learning. \
        1/3 of samples and classes will be used to calculate statistics.
        """

        def categories_count(individual):
            used_categories = []

            for sample in samples:
                category = individual.predict(sample)
                if category is not None:
                    if all([category != c for c in used_categories]):
                        used_categories.append(category)

            return len(used_categories), [individual.get_category_size(category) for category in used_categories]

        # Shuffling of given data.
        data = zip(samples, classes)
        random.shuffle(data)
        samples, classes = zip(*data)
        samples = list(samples)
        classes = list(classes)

        border = len(samples) * 2 / 3

        self.fit(samples[:border], classes[:border])

        categories = [categories_count(agent) for agent in self.result.results['agents']]

        categories_min = 1000
        categories_max = -1
        categories_sum = 0

        avg_agent_sum = 0
        avg_total_sum = 0
        samples_max = 0

        for category_number, list_of_stimuli in categories:
            if category_number > categories_max:
                categories_max = category_number
            if category_number < categories_min:
                categories_min = category_number
            categories_sum += category_number

            if category_number > 0:
                avg_agent_sum += float(sum(list_of_stimuli)) / category_number
                avg_total_sum += sum(list_of_stimuli)
                samples_max = max(samples_max, max(list_of_stimuli))

        category_avenge = float(categories_sum) / len(categories)

        agent_avenge_sample_number = avg_agent_sum / len(categories)
        if categories_sum > 0:
            avenge_sample_number = float(avg_total_sum) / categories_sum
        else:
            avenge_sample_number = 0

        return {"category_minimum": categories_min,
                "category_maximum": categories_max,
                "category_avenge": category_avenge,
                "agent_avenge_sample": agent_avenge_sample_number,
                "avenge_sample_number": avenge_sample_number,
                "max_samples": samples_max,
                "accuracy": self.accuracy(self, samples[border:], classes[border:])}
