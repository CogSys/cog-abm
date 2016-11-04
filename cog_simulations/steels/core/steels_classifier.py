from cog_simulations.cog_abm.ML.core import Classifier

from reactive_unit import ReactiveUnit
from adaptative_network import AdaptiveNetwork


class SteelsClassifier(Classifier):

    def __init__(self):
        self.categories = {}
        self.new_category_id = 0

    def add_category(self, sample=None, class_id=None):
        if class_id is None:
            class_id = self.new_category_id
            self.new_category_id += 1
            adaptive_network = AdaptiveNetwork()
        else:
            adaptive_network = self.categories[class_id]

        if sample is not None:
            adaptive_network.add_reactive_unit(
                ReactiveUnit(sample)
            )

        self.categories[class_id] = adaptive_network
        return class_id

    def del_category(self, category_id):
        del self.categories[category_id]

    def classify(self, sample):
        if len(self.categories) == 0:
            return None
        return max(
            self.categories.iteritems(),
            key=lambda kr: kr[1].reaction(sample)
        )[0]

    def increase_samples_category(self, sample):
        category_id = self.classify(sample)
        self.categories[category_id].increase_sample(sample)

    def forgetting(self):
        for an in self.categories.itervalues():
            an.forgetting()

    def sample_strength(self, category_id, sample):
        return self.categories[category_id].reaction(sample)
