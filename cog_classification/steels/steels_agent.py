from itertools import izip
from sklearn import naive_bayes
from sklearn.utils.validation import NotFittedError
from cog_classification.core.agent import Agent
from cog_classification.steels.lexicon import Lexicon
from cog_classification.steels.sample_storage import SampleStorage


class SteelsAgent(Agent):
    """
    Class representing universal steels agent in the system.

    :param hashable aid: agent's id. Unique identifier of agent.
    :param lexicon lexicon: agent's storage of associations between categories and words.

    Steels agent can associate words with categories but cannot remember samples from environment.
    """

    def __init__(self, aid=None, lexicon=None):
        Agent.__init__(self, aid)
        self.lexicon = lexicon or Lexicon()

    def add_word_to_category(self, word, category):
        return self.lexicon.add_word_to_category(word, category)

    def decrease_weight_word_category(self, word, category):
        self.lexicon.decrease_weight(word, category)

    def find_category_for_word(self, word):
        return self.lexicon.find_category_for_word(word)

    def increase_weight_word_category(self, word, category):
        self.lexicon.increase_weight(word, category)

    def decrease_weights_for_other_categories(self, word, category):
        self.lexicon.decrease_weights_for_other_categories(word, category)

    def decrease_weights_for_other_words(self, word, category):
        self.lexicon.decrease_weights_for_other_words(word, category)

    def find_word_for_category(self, category):
        return self.lexicon.find_word_for_category(category)

    def get_words(self):
        return self.lexicon.get_words()


class SteelsClassificationAgent(SteelsAgent):
    """
    Class implementing steels agent used in classification task.

    :param hashable aid: agent's id. Unique identifier of agent.
    :param Lexicon lexicon: agent's storage of associations between categories and words.
    :param classifier: the classifier that implements three functions: fit, predict and predict_proba.
    :param SampleStorage sample_storage: agent's storage of samples that represents knowledge about environment.

    Steels agent can associate words with categories, remember samples from environment
    and can predict class of given sample.
    """

    def __init__(self, aid=None, lexicon=None, classifier=None, sample_storage=None, alpha=0.99):
        SteelsAgent.__init__(self, aid, lexicon)
        self.classifier = classifier or naive_bayes.GaussianNB()
        self.sample_storage = sample_storage or SampleStorage(alpha=alpha)

    def add_sample(self, sample_index, environment, category=None):
        return self.sample_storage.add_sample(sample_index, environment, category)

    def the_best_sample_for_category(self, category, samples):
        """
        :param hashable category: the category for which sample is chosen.
        :param samples: the list of samples from which the best sample is chosen.
        :type samples: list of sample

        :raise: **IndexError** - if samples is empty.

        :return: the sample with the highest probability of belonging to given category.
        """
        the_best_sample = samples[0]
        the_best_probability = -float('inf')

        # We are looking for a sample that probability of belonging to guesses category is the highest.
        for sample in samples:
            probability = self.get_probability(sample, category)
            if the_best_probability < probability:
                the_best_probability = property
                the_best_sample = sample

        return the_best_sample

    def predict(self, sample):
        """
        Predict class of given specific sample.

        :param sample: the sample that is classified.

        :return: class of sample or None if agent doesn't know any class.
        :rtype: hashable or None

        If agent known only one class, it returns the class. \
        If agent doesn't know any class, it returns None.
        """
        if self.sample_storage.get_categories_size() == 0:
            return None
        elif self.sample_storage.get_categories_size() == 1:
            return self.sample_storage.get_categories()[0]
        else:
            try:
                self.learn()
                # Classifier predicts categories for array of samples and returns array of predicted categories.
                return self.classifier.predict([sample])[0]
            except NotFittedError:
                return None

    def correct_sample_lexicon(self):
        """
        Test if there is any category in lexicon that isn't present in sample storage.

        :raise: **AssertionError** - if there is any category in lexicon that isn't present in sample storage.

        :return: True
        :rtype: bool

        If AssertionError is raised, method prints all categories from lexicon absent in lexicon.
        """

        try:
            assert all([any([c1 == c for c in self.sample_storage.get_categories()])
                        for c1 in self.lexicon.get_categories()])
        except AssertionError:
            print [c for c in self.lexicon.get_categories() if c not in self.sample_storage.get_categories()]
            raise AssertionError

    def forget(self):
        """
        Weakens agent's memory of all known samples and removes categories that become scarcely known.
        """
        self.sample_storage.decrease_weights()
        removed_categories = self.sample_storage.remove_samples_with_low_weights()
        for category in removed_categories:
            self.lexicon.remove_category(category)

    def increase_weights_sample_category(self, sample_index, environment, category):
        self.sample_storage.increase_weights_in_category(sample_index, environment, category)

    def learn(self):
        """
        Teaches classifier using samples and classes from sample storage.
        """
        data, decisions = self.sample_storage.export()
        if len(decisions) > 0 and self.sample_storage.get_categories_size() > 1:
            self.classifier.fit(data, decisions)

    def get_categories_size(self):
        return self.sample_storage.get_categories_size()

    def get_category_class(self, category):
        return self.sample_storage.get_class(category)

    def get_category_size(self, category):
        return len(self.sample_storage.get_category_samples(category))

    def get_probability(self, sample, sample_category):
        """
        :param sample: the sample.
        :param hashable sample_category: the category for which probability of sample belonging is calculated.

        :return: probability of sample belonging to sample category.
        :rtype: float

        Returns 0 if no category known and, if hasn't learn categorisation yet.
        """
        if self.sample_storage.get_categories_size() == 1:
                return sample_category in self.sample_storage.get_categories()
        else:
            try:
                probabilities = self.classifier.predict_proba([sample])
                for category, probability in izip(self.sample_storage.classes, probabilities[0]):
                    if sample_category == category:
                        return probability
            except NotFittedError:
                return 0
