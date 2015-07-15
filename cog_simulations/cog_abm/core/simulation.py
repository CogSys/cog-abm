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

    def __init__(self, graphs=None, interactions=None, environments=None, agents=None, pb=False,
                 colour_order=None):
        """
        @type graphs: List of Maps
        @param graphs: List of Maps with two keys:
            'graph' - Network
            'start' - number of iteration when this Network begin to be used

        @type interactions: List of Maps
        @param interactions: List of Maps with two keys:
            'interaction' - Interaction
            'start' - number of iteration when this Interaction begin to be used

        @type environments: List of Maps
        @param environments: List of Maps with two keys:
            'environment' - Environment
            'start' - number of iteration when this Environment begin to be used

        @type agents: List of Agents
        @param agents: Agents used in simulation.

        @type pb: Bool
        @param pb: Show progress bar.

        @type environments: List of Colours
        @param colour_order: List of Colours in the order used when storing Agents words.
        """
        self.environments = environments
        self.graph = None
        self.graphs = graphs
        self.interaction = None
        self.interactions = interactions
        self.agents = tuple(agents)
        self.statistic = []
        self.dump_often = True
        self.pb = pb
        self.colour_order = colour_order
        print colour_order

    def dump_results(self, iter_num):
        cc = copy.deepcopy(self.agents)
        kr = (iter_num, cc)
        self.statistic.append(kr)
        if self.dump_often:
            f = open("../../results_of_simulation/" + str(iter_num) + ".pout", "wb")
            cPickle.dump(kr, f, PICKLE_PROTOCOL)
            f.close()
            if self.colour_order:
                store_words(self.agents, self.colour_order, str(iter_num)+"words.pout")

    def _change_graph(self, counter):
        for graph in self.graphs:
            if graph["start"] is counter:
                self.graph = graph["graph"]
                break

    def _change_interaction(self, counter):
        for interaction in self.interactions:
            if interaction["start"] is counter:
                self.interaction = interaction["interaction"]
                break

    def _change_environment(self, counter):
        for env in self.environments:
            if env["start"] is counter:
                self.interaction.change_environment(env["environment"])

    def _choose_agents(self):
        if self.interaction.num_agents() == 2:
            a = random.choice(self.agents)
            b = self.graph.get_random_neighbour(a)
            return [a, b]
        else:
            return [random.choice(self.agents)]

    def _start_interaction(self, agents):
        self.interaction.interact(*agents)

    def _do_iterations(self, num_iter, counter):
        for _ in xrange(num_iter):
            self._change_graph(counter)
            self._change_interaction(counter)
            self._change_environment(counter)
            agents = self._choose_agents()
            self._start_interaction(agents)
            counter += 1

    def _do_main_loop(self, iterations, dump_freq):
        start_time = time()
        log.info("Simulation start...")
        it = xrange(iterations // dump_freq)
        counter = 1
        if self.pb:
            it = get_progressbar()(it)
        for i in it:
            self._do_iterations(dump_freq, counter)
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
