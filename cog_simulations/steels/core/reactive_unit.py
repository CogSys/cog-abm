import numpy as np


class ReactiveUnit(object):
    """ Reactive units are used in adaptive networks. """

    def_sigma = 1.

    def __init__(self, central_value, sigma=None):
        self.central_value = central_value
        sigma = sigma or ReactiveUnit.def_sigma
        self.sqr_sig = np.longdouble(-0.5 / (sigma ** 2.))

    def value_for(self, x):
        """ Calculate reaction for given vector """
        a = self.central_value.distance(x) ** 2.
        w = np.exp(a * self.sqr_sig)
        return w

    def __eq__(self,  other):
        if isinstance(other,  ReactiveUnit):
            return other.central_value == self.central_value
        else:
            return False
