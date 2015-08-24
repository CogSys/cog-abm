from itertools import izip

import numpy as np
import random


class Environment:
    """
    Stores samples and their classes.

    :param list samples: List of samples. Not empty.
    :param list classes: List of samples' classes. Not empty.
    :param distance: distance function between two samples.
    :type distance: function(sample, sample)

    Samples and classes should have the same length.
    """

    def __init__(self, samples, classes, distance=None):
        assert samples is not None and classes is not None
        assert not samples == [] and not classes == []
        assert len(samples) == len(classes)

        self.samples = samples
        self.classes = classes

        if distance is None:
            distance = self.standard_distance

        self.distance = distance

    @staticmethod
    def standard_distance(sample1, sample2):
        """
        Calculates standard distance between two samples of numerical values.

        :param iterable sample1: First sample.
        :param iterable sample2: Second sample.

        :return: The calculated distance.
        :rtype: float
        """

        distance = 0
        for v1, v2 in izip(sample1, sample2):
            distance += abs(v1 - v2)

        return distance

    def get_all(self):
        """
        :returns: * List of all samples *(list)*
            * List of all classes *(list)*
        """
        return self.samples, self.classes

    def get_class(self, index):
        """
        Returns class of sample with given index.

        :param long index: The index of the sample whose class is needed.

        :return: Class of sample with given index.
        :rtype: numpy array
        """
        return np.array(self.classes[index])

    def get_random_sample(self):
        """
        Return a random sample from all samples.

        :returns: * Index of drawn sample *(long)*
            * Drawn sample *(list)*
            * Class of drawn sample
        """
        index = random.randrange(len(self.samples))
        sample = self.get_sample(index)
        sample_class = self.get_class(index)
        return index, sample, sample_class

    def get_sample(self, index):
        """
        Returns sample with specified index.

        :param long index: Specified index.

        :return: Sample associated with given index.
        :rtype: numpy array
        """
        return np.array(self.samples[index])

    def get_samples(self, indexes):
        """
        Returns list of samples with given indexes.

        :param iterable indexes: Specified indexes.

        :return: Samples associated with given indexes.
        :rtype: numpy array
        """
        return np.array([self.samples[index] for index in indexes])
