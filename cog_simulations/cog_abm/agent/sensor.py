from cog_simulations.cog_abm.extras.tools import abstract
from cog_simulations.cog_abm.ML.diversity import new_sample_specified_attributes
from cog_simulations.cog_abm.ML.core import normalize_sample_on_nconfig


class Sensor(object):
    """ Basic sensor. """

    def sense(self, item):
        abstract()


class SimpleSensor(Sensor):
    """ Just gives back what he got. """

    def __init__(self, mask=None):
        self.mask = mask

    def sense(self, item):
        if self.mask is None:
            return item
        else:
            return new_sample_specified_attributes(item, self.mask)


class NormalizingSensor(object):

    def __init__(self, norm_conf):
        self.norm_conf = norm_conf

    def sense(self, sample):
        return normalize_sample_on_nconfig(sample,
            self.norm_conf)
