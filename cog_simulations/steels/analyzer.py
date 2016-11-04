import argparse
import sys
import cPickle
import logging

import os

sys.path.append(os.path.dirname(__file__) + '/../')
sys.path.append(os.path.dirname(__file__) + '/../../')
sys.path.append('../')
sys.path.append('../../')

from cog_simulations.cog_abm.extras.tools import get_progressbar
from cog_simulations.steels.metrics import *


def add_arguments(parser_p):

    parser_p.add_argument('-v', '--verbose', dest='verbose', action='count',
                          help="increase verbosity (specify multiple times for more)")

    parser_p.add_argument('-c', '--chart', action="store_true", dest='chart',
                          default=False, help="specifies output to be a chart")

    parser_p.add_argument('-r', '--results_file', action="store", dest='results',
                          help="input file with results. THIS OPTION IS NECESSARY!")

    parser_p.add_argument('--x_label', action="store", dest='x_label',
                          help="Label of x-axis")

    parser_p.add_argument('--y_label', action="store", dest='y_label',
                          help="Label of y-axis")

    parser_p.add_argument('-l', '--log_file', dest='log_file', action='store',
                          help='Name of file in which will be stored log information.')

    parser_p.add_argument('statistics', action="store", nargs='*')


def set_logging_options():
    # Setting log_level and log file whether specified.
    log_level = logging.WARNING

    if arguments.verbose == 1:
        log_level = logging.INFO

    elif arguments.verbose >= 2:
        log_level = logging.DEBUG
    # Set up basic configuration, out to std err with a reasonable default format.
    if arguments.log_file is not None:
        logging.basicConfig(filename=arguments.log_file, level=log_level)
    else:
        logging.basicConfig(level=log_level)

def default(statistic_name):
    if statistic_name[-1] == 'A':
        return lambda agents, iteration: [success_of_agent(agent, statistic_name[:-1]) for agent in agents]
    else:
        return lambda agents, iteration: [success_of_population(agents, iteration, statistic_name)]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program can compute various statistics"
                                                 "from steels experiment results.")
    add_arguments(parser)
    arguments = parser.parse_args()

    set_logging_options()

    with open(arguments.results) as f:
        results, parameters = cPickle.load(f)

    functions_dictionary = {"ccw": lambda agents, iteration: count_category_words(agents, parameters),
                            "CS": lambda agents, iteration: [communication_success_of_population(agents, iteration)],
                            "CSA": lambda agents, iteration: map(communication_success_of_agent, agents),
                            "cv": lambda agents, iteration: [category_variance(agents, iteration)],
                            "DS": lambda agents, iteration: [discrimination_success_of_population(agents, iteration)],
                            "DSA": lambda agents, iteration: map(discrimination_success_of_agent, agents),
                            "it": lambda agents, iteration: [iteration]}

    functions = [functions_dictionary.get(statistic, default(statistic)) for statistic in arguments.statistics]

    pb = get_progressbar()
 #   statistic_values = [[x for f in functions
 #                        for x in f(agents_set.agents.keys(), it)]
 #                       for it, agents_set in pb(results)]
    statistic_values = [[x for f in functions
                         for x in f(agents_set.agents.keys(), it)]
                        for it, agents_set in pb(results)]


    if arguments.chart:
        from cog_simulations.presenter.charts import chart
        data = []
        map(lambda y: data.append((y[0], y[1:])), statistic_values)
        chart(data, arguments.x_label, arguments.y_label)

    else:
        for r in statistic_values:
            print("\t".join(imap(str, r)))
