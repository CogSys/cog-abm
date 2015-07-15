import random
from itertools import izip

from core import Classifier, Sample, split_data


# Methods suposed to introduce diversity:
# * using only subset of attributes
def new_sample_specified_attributes(sample, mask):
    """ mask[i] == True if we want to keep this attribute
    """
    f = lambda v: [x for x, b in izip(v, mask) if b]
    values, meta = f(sample.values), f(sample.meta)
    return Sample(values, meta, cls=sample.cls, cls_meta=sample.cls_meta,
        dist_fun=sample.dist_fun)


def gen_bitmap(length, num_missing):
    mask = [True for _ in xrange(length - num_missing)] + \
           [False for _ in xrange(num_missing)]
    random.shuffle(mask)
    return mask


def random_attribute_selection(samples, num_deleted=2):
    mask = gen_bitmap(len(samples.meta), num_deleted)
    return [new_sample_specified_attributes(s, mask) for s in samples]


# * using only specified ratio of samples in learning
def random_subset_of_samples(samples, ratio):
    return split_data(samples, ratio)[0]


# Wrappers around classifiers to make things easier

class ClassifierSubsetOfAttrs(Classifier):

    def __init__(self, classifier, present_ratio=None, num_missing=None):
        self.classifier = classifier
        self.num_missing = num_missing
        self.present_ratio = present_ratio
        self.attrs_mask = None

    def classify(self, sample):
        sample = new_sample_specified_attributes(sample, self.attrs_mask)
        return self.classifier.classify(sample)

    def classify_p_val(self, sample):
        sample = new_sample_specified_attributes(sample, self.attrs_mask)
        return self.classifier.classify_p_val(sample)

    def class_probabilities(self, sample):
        sample = new_sample_specified_attributes(sample, self.attrs_mask)
        return self.classifier.class_probabilities(sample)

    def _gen_attributes_mask(self, num_attrs):
        if self.present_ratio is not None:
            self.num_missing = int((1. - self.present_ratio) * num_attrs)
        self.attrs_mask = gen_bitmap(num_attrs, self.num_missing)

    def ensure_attrs_mask(self, num_attrs):
        if self.attrs_mask is None or \
                num_attrs != len(self.attrs_mask):
            self._gen_attributes_mask(num_attrs)

    def train(self, samples):
        self.ensure_attrs_mask(len(samples[0].values))
        samples = [new_sample_specified_attributes(s, self.attrs_mask)
            for s in samples]
        self.classifier.train(samples)

    def train_with_weights(self, samples_with_weights):
        self.ensure_attrs_mask(len(samples_with_weights[0][0].values))
        samples = [(new_sample_specified_attributes(s, self.attrs_mask), w)
            for s, w in samples_with_weights]
        self.classifier.train_with_weights(samples)


class ClassifierSubsetOfTraining(Classifier):

    def __init__(self, classifier, present_ratio=None, num_missing=None):
        self.classifier = classifier
        self.num_missing = num_missing
        self.present_ratio = present_ratio
        self.attrs_mask = None

    def classify(self, sample):
        return self.classifier.classify(sample)

    def classify_p_val(self, sample):
        return self.classifier.classify_p_val(sample)

    def class_probabilities(self, sample):
        return self.classifier.class_probabilities(sample)

    def _generate_subset(self, samples):
        num = len(samples)
        if self.present_ratio is not None:
            num_to_learn = int(self.present_ratio * num)
        else:
            num_to_learn = max(0, num - self.num_missing)

        samples = [x for x in samples]
        random.shuffle(samples)
        samples = samples[:num_to_learn]
        return samples

    def train(self, samples):
        samples_subset = self._generate_subset(samples)
        self.classifier.train(samples_subset)

    def train_with_weights(self, samples_with_weights):
        samples_subset = self._generate_subset(samples_with_weights)
        self.classifier.train_with_weights(samples_subset)
