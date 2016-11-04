"""
Most useful things connected with ML
"""
import copy

from itertools import izip
from random import shuffle
from math import fsum

from scipy.io.arff import loadarff

from cog_simulations.cog_abm.extras.tools import flatten


class Classifier(object):

    def classify(self, sample):
        pass

    def classify_p_val(self, sample):
        """
        Returns tuple with class and probability of sample belonging to it
        """
        pass

    def class_probabilities(self, sample):
        """
        Returns dict with mapping class->probability that sample belongs to it
        """
        pass

    def train(self, samples):
        pass

    def train_with_weights(self, samples_with_weights):
        """ samples_with_weights should be [(sample, weight), ... ]
        By default we ignore weights"""
        self.train((sample for sample, weight in samples_with_weights))

    def clone(self):
        """
        Returns copy of classifier. This is default implementation.
        Should be overriden in subclasses.

        @rtype: Classifier
        @return: New instance of classifier.
        """
        return copy.deepcopy(self)


class Attribute(object):

    ID = None
    """ This class field is for id when putting some conversion method in dict
    """

    def get_value(self, value):
        ''' value is inner representation
        '''
        pass

    def set_value(self, value):
        ''' value is outer representation
        '''
        return value

    def __eq__(self, other):
        return self.ID == other.ID

    def dist(self, value1, value2):
        ''' Calculates distance between
            two values of this attribute
        '''
        pass


class NumericAttribute(Attribute):

    ID = "NumericAttribute"

    def get_value(self, value):
        return value

    def dist(self, value1, value2):
        return abs(value1 - value2)


class NominalAttribute(Attribute):

    ID = "NominalAttribute"

    def __init__(self, symbols):
        """
        Symbols should be strings!
        For example Orange doesn't support any other format
        """
        symbols = [str(s) for s in symbols]
        self.symbols = tuple(s for s in symbols)
        self.mapping = dict(reversed(x) for x in enumerate(self.symbols))
        self.tmp_rng = set(xrange(len(self.symbols)))

    def get_symbol(self, idx):
        return self.symbols[idx]

    def get_idx(self, symbol):
        return self.mapping[str(symbol)]

    def get_value(self, value):
        return self.get_symbol(value)

    def set_value(self, value):
        return self.set_symbol(value)

    def set_symbol(self, symbol):
        return self.get_idx(symbol)

    def __eq__(self, other):
        return super(NominalAttribute, self).__eq__(other) and \
            set(self.symbols) == set(other.symbols)

    def dist(self, value1, value2):
        return int(value1 != value2)


class Sample(object):

    def __init__(self, values, meta=None, cls=None, cls_meta=None,
                 dist_fun=None, last_is_class=False, cls_idx=None):
        self.values = values[:]
        self.meta = meta or [NumericAttribute() for _ in values]

        if last_is_class or cls_idx is not None:
            if last_is_class:
                cls_idx = -1
            self.cls_meta = self.meta[cls_idx]
            self.cls = self.values[cls_idx]
            self.meta = self.meta[:]
            del self.values[cls_idx], self.meta[cls_idx]
        else:
            self.cls = cls
            self.cls_meta = cls_meta

        self.dist_fun = dist_fun or get_default_dist_fun(self.meta)

    def get_cls(self):
        if self.cls_meta is None or self.cls is None:
            return None

        return self.cls_meta.get_value(self.cls)

    def get_values(self):
        return [m.get_value(v) for v, m in izip(self.values, self.meta)]

    def distance(self, other):
        return self.dist_fun(self, other)

    def __eq__(self, other):
        return self.cls == other.cls and \
                self.cls_meta == other.cls_meta and \
                self.meta == other.meta and \
                self.values == other.values

    def __hash__(self):
        return 3 * hash(tuple(self.values)) + 5 * hash(self.cls)

    def __str__(self):
        return "({0}, {1})".format(str(self.get_values()), self.get_cls())

    def __repr__(self):
        return str(self)

    def copy_basic(self):
        return Sample(self.values, self.meta, dist_fun=self.dist_fun)

    def copy_full(self):
        return Sample(self.values, self.meta, self.cls, self.cls_meta,
                self.dist_fun)

    def copy_set_cls(self, cls, meta):
        s = self.copy_basic()
        s.cls_meta = meta
        s.cls = meta.set_value(cls)
        return s


def get_default_dist_fun(meta):
    if all(attr.ID == NumericAttribute.ID for attr in meta):
        return euclidean_distance
    return almost_euclidean_distance


#Sample distance functions
def non_sqrted_euclidean_distance(sx, sy):
    return fsum([
        (x - y) * (x - y) for x, y in izip(sx.get_values(), sy.get_values())
        ])


def euclidean_distance(sx, sy):
    return non_sqrted_euclidean_distance(sx, sy) ** 0.5


def almost_non_squered_euclidean_distance(sx, sy):
    return fsum(meta.dist(x_val, y_val)
        for meta, x_val, y_val in
        izip(sx.meta, sx.get_values(), sy.get_values()))


def almost_euclidean_distance(sx, sy):
    return almost_non_squered_euclidean_distance(sx, sy) ** 0.5


def load_samples_arff(file_name, last_is_class=False, look_for_cls=True):
    a_data, a_meta = loadarff(file_name)
    names = a_meta.names()

    attr = {"nominal": lambda attrs: NominalAttribute(attrs),
            "numeric": lambda _: NumericAttribute()}

    gen = (a_meta[n] for n in names)
    meta = [attr[a[0]](a[1]) for a in gen]
    cls_idx = None
    if look_for_cls:
        for i, name in enumerate(names):
            if a_meta[name][0] == "nominal" and name.lower() == "class":
                cls_idx = i
                break

    def create_sample(s):
        values = [mi.set_value(vi) for mi, vi in izip(meta, s)]
        return \
            Sample(values, meta, last_is_class=last_is_class, cls_idx=cls_idx)

    return [create_sample(s) for s in a_data]


def normalize_attribute_on_config(sample, attr_idx, diff):
    attr = sample.meta[attr_idx]
    old_val = attr.get_value(sample.values[attr_idx])
    sample.values[attr_idx] = attr.set_value(old_val / diff)


def normalize_numeric_attribute(attr_idx, samples):
    attr = samples[0].meta[attr_idx]
    values = [attr.get_value(s.values[attr_idx])
            for s in samples]
    diff = float(max(values) - min(values))
    if diff == 0.:
        return None

    for sample in samples:
        normalize_attribute_on_config(sample, attr_idx, diff)

    return diff


def normalize_nominal_attribute(attr_idx, samples):
    return None


NORMALIZATION_CONFIG = {
    NumericAttribute.ID: normalize_numeric_attribute,
    NominalAttribute.ID: normalize_nominal_attribute,
}


def calc_normalization_attriubte_conf(attr_idx, samples):
    attr = samples[0].meta[attr_idx]
    if attr.ID != NumericAttribute.ID:
        return None
    values = [attr.get_value(s.values[attr_idx])
            for s in samples]
    diff = float(max(values) - min(values))
    if diff == 0.:
        return None
    return diff


def calc_normalization_config(samples):
    return [calc_normalization_attriubte_conf(i, samples)
        for i in xrange(len(samples[0].values))]


def normalize_samples(samples, config=None):
    config = config or NORMALIZATION_CONFIG
    norm_conf = [NORMALIZATION_CONFIG[meta.ID](i, samples)
            for i, meta in enumerate(samples[0].meta)]
    return norm_conf


def normalize_sample_on_nconfig(sample, nconfig):
    sample = sample.copy_full()
    for i, conf_params in enumerate(nconfig):
        if conf_params is not None:
            normalize_attribute_on_config(sample,
                i, conf_params)
    return sample


def split_data(data, train_ratio=2. / 3.):
    """ data - samples to split into two sets: train and test
    train_ratio - real number in [0,1]

    returns (train, test) - pair of data sets
    """
    tmp = [s for s in data]
    shuffle(tmp)
    train = [s for i, s in enumerate(tmp) if i < train_ratio * len(tmp)]
    test = [s for i, s in enumerate(tmp) if i >= train_ratio * len(tmp)]
    return (train, test)


def split_data_cv(data, folds=8):
    """ data - samples to split into two sets *folds* times

    returns [(train, test), ...]  - list of pairs of data sets
    """
    tmp = [s for s in data]
    shuffle(tmp)
    N = len(tmp)
    M = N / folds
    overflow = N % folds
    splits = []
    i = 0
    while i < N:
        n = M
        if overflow > 0:
            overflow -= 1
            n += 1
        split = tmp[i:i + n]
        splits.append(split)
        i += n

    return [(flatten(splits[:i] + splits[i + 1:]), splits[i])
        for i in xrange(folds)]
