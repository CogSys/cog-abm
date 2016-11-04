from itertools import izip

import numpy as np


class SampleStorage:
    """
    Storage of samples that represents knowledge about environment.

    :param float alpha: how fast samples are forgotten. Values from 0 (total sclerosis) to 1 (perfect memory).
    :param float beta: how much weights of samples will be increased. Values from 0 (no strengthening) to infinity.
    :param float sigma: affects how factor of similarity affects strengthening of weights. \
        Value form 0 (similarity doesn't affects strengthening) \
        to infinity (the less similar samples the weaker strengthen).
    :param float max_weight: the maximum weight of sample. Value from 0 to infinity.
    :param float new_weight: the weight of new sample added to sample storage if no other value were given. \
        Value from 0 to max weight.
    :param float forgetting_threshold: the samples with lower weight value than forgetting threshold value are removed.\
        Value from 0 to max weight.
    :param distance: default function which can compute distance between two samples.
    :type distance: function(sample, sample)

    Sample storage provides a way to represent samples known by agent and gives you a easy way to export this samples
    to format designed for machine learning algorithms.

    Every sample is associated with class of sample, environment of origin,
    category of sample storage (one sample can be associated with more than one category),
    weight of association to this category, which can affect removing of sample if weight is lower than fixed
    forgetting threshold.

    Each sample is represented as sample index in environment of origin at which is stored.
    It is result of concern about performance and memory usage.

    Each sample of the same category in sample storage has the same class. Every try to add sample with different
    class will result in creating new category and adding this sample to it.

    Weights can be increased and decreased but it will not remove samples from category directly. Even if weight of
    sample will drop to 0 (minimum weight), sample will be still part of category. To remove sample with weights lower
    than forgetting threshold, should be used methods remove weak samples and remove weak samples from category.

    Sample storage is implementation of the class described in Konrad Kurdej's master's thesis:
    "Modelowanie procesow poznawczych: konsensusowa metoda klasyfikacji z komunikacja miedzy agentami".
    """

    def __init__(self, alpha=0.99, beta=1, sigma=1, new_weight=1, max_weight=1,
                 forgetting_threshold=0.05, distance=None):

        self.category_name = 0

        self.alpha = alpha
        assert alpha >= 0
        assert alpha <= 1

        self.beta = beta
        assert beta >= 0

        self.sigma = sigma
        assert sigma >= 0

        self.max_weight = max_weight
        assert max_weight >= 0

        self.new_weight = new_weight
        assert new_weight >= 0
        assert new_weight <= max_weight

        self.forgetting_threshold = forgetting_threshold
        assert new_weight >= 0
        assert new_weight <= max_weight

        # Distance is used only in increase weights.
        self.distance = distance

        # Categories: {category: {environment: ([sample_indexes], [sample_weight])}}
        self.categories = {}
        # Classes: {category: sample_class}
        self.classes = {}

    def add_sample(self, sample_index, environment, category=None, sample_weight=None):
        """
        Adds sample to sample storage.

        :param sample_index: the index of sample in environment.
        :type sample_index: int or long
        :param Environment environment: the environment from which sample origins.
        :param hashable category: the category which sample will be add.
        :param float sample_weight: the initial weight of sample. (>=0; <=max_weight)

        :raise IndexError: if the sample index doesn't correspond to any sample in the environment.
        :raise TypeError: if the category isn't hashable.
        :raise AssertionError: if the sample_weight out of range.

        :return: the name of category which sample was added.
        :rtype: hashable

        | Adds the sample to given category. If no category is given, adds sample to new created category.
        | If sample would be add to category, which class is different, then adds sample to new created category.
        | If sample has been already added to any category, then method do nothing.

        | Sample has sample_weight if given or default new_weight of sample storage.
        """

        if sample_weight is None:
            sample_weight = self.new_weight
        else:
            assert sample_weight >= 0
            assert sample_weight <= self.max_weight

        sample_class = environment.get_class(sample_index)

        for checked_category in self.categories:
            if self.sample_in_category(sample_index, environment, checked_category):
                """
                We are sure that if sample is in storage in checked category
                then it won't be add to any other category by replacing category by checked category.
                """
                category = checked_category

        if category in self.categories:
            if sample_class == self.classes[category]:
                # No difference between class of sample and class of category.
                if not self.sample_in_category(sample_index, environment, category):
                    # Adding new sample to category.
                    self.set_weight(environment, category, sample_weight, sample_index=sample_index)
            else:
                # There is difference in class of sample and class of category.
                # So we are adding sample to empty category (it forces creation of new category for sample).
                return self.add_sample(sample_index, environment, sample_weight=sample_weight)
        else:
            # No such category in sample storage.
            # So we create new category for sample (and new name if category is None).
            category = self.create_new_category(sample_class, category)
            self.categories[category][environment] = ([], [])
            self.set_weight(environment, category, sample_weight, sample_index=sample_index)

        return category

    def create_new_category(self, sample_class, category=None):
        """
        Creates new empty category in sample storage.

        :param sample_class: the class of all samples in this category.
        :param hashable category: the name of category.

        :raise: **AssertionError** - if category has already been in sample storage categories.

        :return: the name of category.
        :rtype: hashable
        """

        if category is None:
            # We create new name for category.

            # First we finds the name that wasn't used.
            name_in_categories = True
            name = None

            while name_in_categories:
                name_in_categories = False
                name = "Category number: " + str(self.category_name)
                for category_name in self.categories:
                    if category_name == name:
                        name_in_categories = True
                        break
                self.category_name += 1

            category = name
            # After while loop we didn't increase self.category_name because after finding unique name
            # we increased this value on the end of while loop.
        else:
            assert category not in self.categories

        self.categories[category] = {}
        self.classes[category] = sample_class

        assert category is not None

        return category

    def decrease_weights(self):
        """
        Decrease weights in sample storage.

        | Weights of every sample in category will be decreased according to alpha value.
        | The weights will never drop below 0.
        | This method didn't remove any sample.
        """
        for category in self.get_categories():
            self.decrease_weights_in_category(category)

    def decrease_weights_in_category(self, category):
        """
        Decrease weights in category.

        :param hashable category: the category which sample will be add.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        | Weights of every sample in category will be decreased according to alpha value.
        | The weights will never drop below 0.
        | This method didn't remove any sample.
        """

        the_category = self.categories[category]

        for environment in the_category:
            _, weights = the_category[environment]
            for i in range(len(weights)):
                weights[i] = max(0, self.alpha * weights[i])

    def empty(self):
        """
        Tests if sample storage is empty.
        """

        # There isn't sample without category so, if number of categories equals zero then sample storage is empty.
        return len(self.categories) == 0

    def export(self):
        """
        Returns all sample storage data.

        :returns: * lists of all attributes of every sample *(numpy array)*
            * list of classes of every sample *(numpy array)*

        List of attributes and class at given index of returned numpy array are parallel.
        """
        samples = []
        samples_categories = []

        for category in self.get_categories():
            the_category = self.categories[category]

            single_category_samples = []
            for environment in the_category:
                sample_indexes, _ = the_category[environment]
                for index in sample_indexes:
                    single_category_samples.append(environment.get_sample(index))

            for sample in single_category_samples:
                samples.append(sample)
            samples_categories += [category] * len(single_category_samples)

        return np.array(samples), np.array(samples_categories)

    def get_categories(self):
        """
        :return: list of all categories names of sample storage.
        :rtype: list
        """
        return self.categories.keys()

    def get_categories_size(self):
        """
        :return: number of categories in the sample storage.
        :rtype: long
        """
        return len(self.categories)

    def get_category_samples(self, category):
        """
        :param hashable category: the category which samples weights will be increased.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        :return: list of all samples in category.
        :rtype: list of tuples - (sample_index, environment, weight)

                 - sample_index (int or long) - The index of sample in environment.

                 - environment (Environment) - The environment from which sample origins.

                 - weight (float) - The weight of sample in category.
        """
        samples = []

        the_category = self.categories[category]
        for environment in the_category:
            sample_indexes, weights = the_category[environment]
            for sample_index, weight in izip(sample_indexes, weights):
                samples.append((sample_index, environment, weight))

        return samples

    def get_category_samples_size(self, category):
        """
        :param hashable category: the category which samples weights will be increased.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        :return: number of samples in the category.
        :rtype: long
        """
        size = 0

        the_category = self.categories[category]
        for environment in the_category:
            sample_indexes, _ = the_category[environment]
            size += len(sample_indexes)

        return size

    def get_class(self, category):
        """
        :param hashable category: the category.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        :return: class of given category.
        """
        return self.classes[category]

    def increase_weights_in_category(self, sample_index, environment, category):
        """
        Increase the weights of samples in category.

        :param sample_index: the index of sample in environment.
        :type sample_index: int or long
        :param Environment environment: the environment from which sample origins.
        :param hashable category: the category which samples weights will be increased.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        | Weights will be increased according to their distance to sample modified by sigma and beta.
        | Weights will never rise above max weight.
        | This method **doesn't** add sample to category.
        """
        the_category = self.categories[category]
        sample = environment.get_sample(sample_index)

        for environment_local in the_category:

            sample_indexes, weights = the_category[environment_local]

            for i in range(len(sample_indexes)):

                category_sample = environment_local.get_sample(sample_indexes[i])

                if self.distance is None:
                    distance = environment.distance(category_sample, sample)
                else:
                    distance = self.distance(category_sample, sample)

                weight_change = self.beta * 0.1 ** (self.sigma * distance)
                new_weight = min(weights[i] + weight_change, self.max_weight)

                # We don't change value directly because it will be easier to change only set weight if some
                # changes will be necessary.
                self.set_weight(environment, category, new_weight, index=i)

    def remove_category(self, category):
        """
        Removes category and all its samples from sample storage.

        :param hashable category: the removed category.
        """
        try:
            self.categories.pop(category)
            self.classes.pop(category)
        except KeyError:
            for c in self.categories:
                if category == c:
                    category = c
                    break

            self.categories.pop(category)
            self.classes.pop(category)

    def remove_sample_from_category(self, environment, category, sample_index=None, index=None):
        """
        Removes sample from given category.

        :param Environment environment: the environment from which removed sample origins.
        :param hashable category: the category of removed sample.
        :param sample_index: the index of sample in environment.
        :type sample_index: int or long
        :param index: the index of sample in category environment list.

        :raise TypeError: if both sample_index and index aren't defined.
        :raise KeyError: if category doesn't exist in sample storage.

        :returns: the name of removed category or None if category hasn't removed.
        :rtype: hashable or None

        | **Sample or index should be specified.**
        | If it was the last sample in the category, then category is removed, too.
        """

        the_category = self.categories[category]

        sample_indexes, weights = the_category[environment]

        if index is None:
            # We must find index of sample:
            for i in range(len(sample_indexes)):
                if sample_indexes[i] == sample_index:
                    index = i
                    break

        sample_indexes.pop(index)
        weights.pop(index)

        if self.get_category_samples_size(category) == 0:
            self.remove_category(category)
            return category
        else:
            return None

    def remove_samples_with_low_weights(self):
        """
        Removes every sample with low weight.

        :returns: list of names of all removed category. (Can be empty.)
        :rtype: hashable or None

        | Removed will be samples with weight lower than forgetting threshold.
        | It removes classes that lose all samples.

        """
        removed_categories = [self.remove_samples_with_low_weights_from_category(category)
                              for category in self.get_categories()]
        return [category for category in removed_categories if category is not None]

    def remove_samples_with_low_weights_from_category(self, category):
        """
        Removes every sample in category with low weight.

        :param hashable category: the category which samples weights will be increased.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        :returns: the name of removed category or None if category hasn't removed.
        :rtype: hashable or None

        | Removed will be samples with weight lower than forgetting threshold.
        | It can remove the class if it loses all samples.
        """

        the_category = self.categories[category]
        removed_category = None
        for environment in the_category:

            to_remove = []
            sample_indexes, weights = the_category[environment]
            for i, (_, weight) in enumerate(izip(sample_indexes, weights)):
                if weight < self.forgetting_threshold:
                    to_remove.append(i)

            to_remove = sorted(to_remove, reverse=True)
            for i in to_remove:
                removed_category = self.remove_sample_from_category(environment, category, index=i)

        return removed_category

    def sample_in_category(self, sample_index, environment, category):
        """
        Checks if given sample_index is in category.

        :param sample_index: the index of sample in environment.
        :type sample_index: int or long
        :param Environment environment: the environment from which sample origins.
        :param hashable category: the category which samples weights will be increased.

        :raise: **KeyError** - if category doesn't exist in sample storage.

        :return: True if sample is in category, otherwise False.
        :rtype: bool
        """
        if environment not in self.categories[category]:
            return False
        else:
            sample_indexes, _ = self.categories[category][environment]
            return sample_index in sample_indexes

    def set_weight(self, environment, category, new_weight, sample_index=None, index=None):
        """
        Sets weight of sample in category.

        :param Environment environment: the environment from which sample origins.
        :param hashable category: the category of sample.
        :param float new_weight: the weight to be set for sample in category. (>=0, <=max_weight)
        :param sample_index: the index of sample in environment.
        :type sample_index: int or long
        :param index: the index of sample in category environment list.

        :raise KeyError: if category doesn't exist in sample storage.
        :raise AssertionError: if new_weight is out of range.
        :raise AssertionError: if both sample_index and index aren't defined.

        | **Sample or index should be specified.**
        | If sample isn't in category then it is added to it with weight equals to new_weight.
        """
        assert new_weight >= 0
        assert new_weight <= self.max_weight

        assert category is not None

        the_category = self.categories[category]
        if environment not in the_category:
                the_category[environment] = ([], [])

        sample_indexes, weights = the_category[environment]

        if index is not None:
            # We know which weight change.
            weights[index] = new_weight
        else:
            assert sample_index is not None
            # We must find index of sample_index.
            found = False
            for i, (index, weight) in enumerate(izip(sample_indexes, weights)):
                if index == sample_index:
                    weights[i] = new_weight
                    found = True
                    break

            if not found:
                sample_indexes.append(sample_index)
                weights.append(new_weight)
