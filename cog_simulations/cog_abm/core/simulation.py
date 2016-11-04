"""
Module providing flow control in simulation
"""
import random
import logging
from time import time
import copy
import cPickle
from ..extras.tools import get_progressbar
from ..extras.words_storage import store_words

log = logging.getLogger('COG-ABM')

PICKLE_PROTOCOL = cPickle.HIGHEST_PROTOCOL


class Simulation(object):
    """
    This class defines what happens and when.
    """

    def __init__(self, interactions_sets=None, pb=False, colour_order=None, dump_often=None):
        """
        @type interactions_sets: Map of Lists of Interactions
        @param interactions_sets: List of Maps with two keys:
            'graph' - List of Interactions
            'start' - number of iteration when this List of Interactions begin to be used

        @type pb: Bool
        @param pb: Show progress bar.

        @param colour_order: List of Colours in the order used when storing Agents words.
        """
        self.iteration_counter = 1

        self.interactions_set = interactions_sets[1]
        self.interactions_sets = interactions_sets

        self.statistic = []
        self.dump_often = dump_often
        self.pb = True
        self.colour_order = colour_order

    def dump_results(self, iter_num):
        cc = copy.deepcopy(self.get_agents())
        kr = (iter_num, cc)
        self.statistic.append(kr)
        if self.dump_often:
            f = open(self.dump_often + str(iter_num) + ".pout", "wb")
            cPickle.dump(kr, f, PICKLE_PROTOCOL)
            f.close()
            if self.colour_order:
                store_words(self.get_agents(), self.colour_order, str(iter_num)+"words.pout")

    def get_iteration_counter(self):
        return self.iteration_counter

    def set_colour_order(self, colour_order):
        self.colour_order = colour_order

    def get_agents(self):
        return self.interactions_set[0].agents

    def _change_interactions_set(self):
        if self.iteration_counter in self.interactions_sets:
            self.interactions_set = self.interactions_sets[self.iteration_counter]

    def _do_iterations(self, num_iter):
        for _ in xrange(num_iter):
            self._change_interactions_set()
            for interaction in self.interactions_set:
                interaction.interact()
            self.iteration_counter += 1

    def _do_main_loop(self, iterations, dump_freq):
        start_time = time()
        log.info("Simulation start...")
        it = xrange(iterations // dump_freq)
        if self.pb:
            it = get_progressbar()(it)
        for i in it:
            self._do_iterations(dump_freq)
            self.dump_results((i + 1) * dump_freq)

        log.info("Simulation end. Total time: " + str(time() - start_time))

    def continue_(self, iterations=1000, dump_freq=10):
        self._do_main_loop(iterations, dump_freq)
        return self.statistic

    def run(self, iterations=1000, dump_freq=10):
        """ Begins simulation. """
        self.dump_results(0)
        self._do_main_loop(iterations, dump_freq)
        return self.statistic
