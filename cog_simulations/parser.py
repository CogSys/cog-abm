"""
Module provides parser for json documents.
"""
import json
import cPickle
import os.path

from cog_simulations.cog_abm.core.network import Network
from cog_simulations.cog_abm.generators.graph_generator import graph_generator


class Parser(object):
    """
    Parser class.

    Parser provides methods used to handle simulation input when given in json.

    @sort: __init__
    """

    def __init__(self):
        """ Initialize parser. """

    def parse_simulation(self, source):
        """
        Parse simulation parameters given in json document.

        @type source: String
        @param source: Simulation JSON document directory.

        @rtype: Dictionary
        @return: Simulation parameters created from json document.
        """

        if source is None:
            return None

        source_name = source
        with open(source, 'r') as f:
            source = json.loads(f.read())

        dictionary = {}

        self.load_parameters(dictionary, source)
        self.load_agents(dictionary, source)

        self.load_interactions_sets(dictionary, source, source_name)

        return dictionary

    def load_interactions_sets(self, dictionary, source, source_name):
        interactions_sets = {}

        for start, interactions_set in source["interactions_sets"].iteritems():
            interactions_sets[int(start)] = self.load_interactions_set(interactions_set, source_name, dictionary)

        dictionary["interactions_sets"] = interactions_sets

    def load_interactions_set(self, source, source_name, dictionary):

        for interaction in source:
            interaction["agents"] = self.load_network(interaction["network"], source_name, dictionary)
            interaction["environment"] = self.load_environment(interaction["environment"], source_name)

        return source

    def load_network(self, source, source_name, dictionary):
        g_type = self.value_if_exist("type", source)
        network_source = self.value_if_exist("source", source)
        if network_source is not None and not os.path.isabs(network_source):
            network_source = "%s/%s" % (os.path.dirname(source_name), network_source)
        g = graph_generator(g_type, len(dictionary["agents"]), network_source)
        return Network(g)

    def load_environment(self, source, source_name):
        environment_source = self.value_if_exist("source", source)
        if not os.path.isabs(environment_source):
            environment_source = "%s/%s" % (os.path.dirname(source_name), environment_source)
        source["source"] = self.parse_environment(environment_source)
        return source

    def load_parameters(self, dictionary, source):
        """ Load general simulation parameters given in source. """

        parameters = ["dump_freq", "num_iter", "alpha", "beta", "sigma"]
        for p in parameters:
            self.load_to_dictionary(dictionary, p, source)

    def load_agents(self, dictionary, source):
        """ Load simulation Agents given in source. """

        agents_source = self.value_if_exist("agents", source)
        agents = []

        if agents_source is not None:
            with open(agents_source, 'r') as f:
                agents_data = json.loads(f.read())
            source["num_agents"] = len(agents_data)
            dictionary["num_agents"] = source["num_agents"]
            for agent in agents_data:
                agents.append(agent)
        else:
            num_agents = self.value_if_exist("num_agents", source)
            dictionary["num_agents"] = num_agents
            for i in range(num_agents):
                agents.append({"node_name": i})

        dictionary["agents"] = agents

    @staticmethod
    def parse_environment(doc):
        """ Parse environment parameters given in json document. """
        with open(doc, 'r') as f:
            environment = json.loads(f.read())

        return environment

    @staticmethod
    def load_to_dictionary(dictionary, key, source, obligatory=False, function=None):
        """
        Loads value from key in source to key in dictionary.

        @type dictionary: Map
        @param dictionary: Map which is loaded value.

        @type key: String
        @param key: Key of value loaded.

        @type source: Map
        @param source: Map with value.

        @type obligatory: Bool
        @param obligatory: Key have to be in source.

        @type obligatory: Function
        @param obligatory: Function that have to be used on value before loading into dictionary.
        """
        if key in source:
            if function is None:
                dictionary[key] = source[key]
            else:
                dictionary[key] = function(source[key])
        elif obligatory:
            raise Exception("Information about " + key + " should be written in simulation file.")

    @staticmethod
    def value_if_exist(key, source, function=None):
        """
        Reads value assigned to key from source. If source doesn't contain key return None.

        @type key: String
        @param key: Key of value read.

        @type source: Map
        @param source: Map with value.

        @type function: function
        @param function: Function that have to be used on value after reading.

        @rtype: Any
        @return: Value assigned to key in source or None.
        """
        if key in source:
            if function is None:
                return source[key]
            else:
                return function(source[key])
        else:
            return None
