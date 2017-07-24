"""
Module providing environment and it's functionality
"""

import numpy as np
from sklearn.neighbors import KDTree

from random import choice, shuffle
from itertools import imap


class StimuliChooser(object):

    def __init__(self, n=None):
        self.n = n

    def get_stimulus(self, stimuli):
        return choice(stimuli)

    def get_stimuli(self, stimuli, stimuli_tree=None, n=None):
        pass


class RandomStimuliChooser(StimuliChooser):

    def __init__(self, n=None, use_distance=False, distance=50.):
        super(RandomStimuliChooser, self).__init__(n)
        self.use_distance = use_distance
        self.distance = distance

    def get_stimuli(self, stimuli, stimuli_tree=None, n=None):
        """
        Be careful with this - can take some time when using the distance!
        """
        n = n or self.n
        if not self.use_distance:
            return [self.get_stimulus(stimuli) for _ in xrange(n)]

        dist, get_stimulus = self.distance, self.get_stimulus
        # ^^ abandoning dots - small speed up ..
        for _ in xrange(250):
            ret = []
            avail_stimuli = np.ones(len(stimuli), dtype=np.bool)
            for _ in xrange(n):
                ret.append(get_stimulus(stimuli[avail_stimuli]))
                apoint = (ret[-1].L, ret[-1].a, ret[-1].b)
                avail_stimuli[stimuli_tree.query_radius([apoint], 50.0)[0]] = 0
                if sum(avail_stimuli) == 0:
                    break
            if len(ret) == n:
                shuffle(ret)
                return ret
        raise Exception("Couldn't get samples separated by such distance!")

    def __repr__(self):
        return "RandomStimuliChooser: use_distance:%s; distance:%s" % \
            (self.use_distance, self.distance)


class OneDifferentClass(StimuliChooser):
    """
    This will return first sample of class different than others.
    This is important if we have binary classification and contex of size 4
    """

    def __init__(self, n=None):
        self.n = n

    def get_stimuli(self, stimuli, stimuli_tree=None, n=None):
        n = n or self.n
        for _ in xrange(100):
            ret = [self.get_stimulus(stimuli)]
            cls = ret[0].get_cls()
            for _ in xrange(n - 1):
                try_limit = 100
                while try_limit > 0:
                    tmp = self.get_stimulus(stimuli)
                    if cls != tmp.get_cls():
                        break
                    try_limit -= 1
                if cls == tmp.get_cls():
                    break
                ret.append(tmp)
            if len(ret) == n:
                return ret
        raise Exception("Couldn't get samples in different classes")

    def __repr__(self):
        return "OneDifferentClass"


class Environment(object):
    """
    Basic class for stimuli.
    It's main function is to provide stimuli for agents
    """

    def __init__(self, stimuli, stimuli_chooser=None, colour_order=None,
                 metric='euclidean'):
        """
        Initialize environment

        @param stimuli: initial set of stimuli
        @type stimuli: sequence
        @param colour_order: list of distinct stimuli in order of saving to a file (if needed)
        @type colour_order: sequence
        """
        self.stimuli = np.array(stimuli)
        self.stimuli_chooser = stimuli_chooser or RandomStimuliChooser(1)
        self.colour_order = colour_order
        self.ball_tree = KDTree([(s.L, s.a, s.b) for s in stimuli],
                                metric=metric)

    def get_stimulus(self):
        """
        Gives stimulus from the set of available stimuli

        @return: random stimulus
        @rtype: Stimulus
        """
        return self.stimuli_chooser.get_stimulus(self.stimuli)

    def get_all_stimuli(self):
        """
        Gives set of all stimuli available in the environment

        @return: sequence of stimuli
        @rtype: sequence
        """
        return self.stimuli

    def get_stimuli(self, n):
        return self.stimuli_chooser.get_stimuli(self.stimuli, self.ball_tree, n)
