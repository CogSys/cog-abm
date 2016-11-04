import numpy as np

class AdaptiveNetwork(object):
    """ Adaptive network is some kind of classifier. """

    def_alpha = 0.1
    def_beta = 1.

    def __init__(self,  reactive_units=None, alpha=None, beta=None):
        """ Must be with weights ! """
        self.units = reactive_units or []
        self.alpha = np.longdouble(alpha or AdaptiveNetwork.def_alpha)
        self.beta = np.longdouble(beta or AdaptiveNetwork.def_beta)

    def _index_of(self, unit):
        """
        Finds index of given unit.
        Returns -1 if there is no such unit in this network.
        """
        for i, (u, _) in enumerate(self.units):
            if u == unit:
                return i
        return -1

    def add_reactive_unit(self, unit, weight=1.):
        index = self._index_of(unit)
        weight = np.longdouble(weight)
        if index == -1:
            self.units.append((unit, weight))
        else:
            self.units[index] = (unit, weight)

    def reaction(self, data):
        return sum((w * u.value_for(data) for u, w in self.units))

    def _update_units(self, update):
        tmp = [update(u, w) for u, w in self.units]
        self.units = filter(lambda x: x is not None,  tmp)

    def remove_low_units(self, threshold=0.1 ** 30):
        self.units = [(u, w) for u, w in self.units if w >= threshold]

    def increase_sample(self, sample):
        update = lambda u, w: (u,
                               # We don't want weight to exceed 1.
                               min(np.longdouble(1.), w + self.beta * u.value_for(sample)))
        self._update_units(update)

    def forgetting(self):
        self._update_units(lambda u, w: (u, self.alpha * w))
