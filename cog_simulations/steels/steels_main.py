import argparse
import sys
import logging
import cPickle
from time import localtime, strftime

sys.path.append('../../')
sys.path.append('../')
sys.path.append('')

from cog_simulations.parser import Parser
from cog_simulations.steels.core.steels_experiment import steels_experiment


def add_arguments(pars):

    pars.add_argument('-s', '--simulation_file', dest='simulation_file', action='store',
                      help='Name of file with all simulation parameters. '
                           'You should choose this option or option -c.')

    pars.add_argument('-c', '--load_simulation', dest='load_simulation', action='store',
                      help='Name of file in which is stimulation to continue. '
                           'You should choose this option or option -s.')

    pars.add_argument('-r', '--results_file', dest='results_file', action='store',
                      default=strftime('experiment_%Y%m%d_%H_%M_%S.result', localtime()),
                      help='Name of results file. Default: experiment_date.result')

    pars.add_argument('-ss', '--save_simulation', dest='save_simulation', action='store',
                      help='Name of file in which will be stored simulation after its run. '
                           'Default: only results of simulation will be saved.')

    pars.add_argument('-d', '--dump', dest='dump', action='store',
                      help='Name of beginning of dump files.')

    pars.add_argument('-p', '--parameters', dest='parameters', action='store',
                      help='Name of file in which are parameters used in stimulation continuation.')

    pars.add_argument('-n', '--load_network', dest='networks', action='store',
                      help='Name of file in which are networks used in stimulation continuation.')

    pars.add_argument('-e', '--load_environment', dest='environments', action='store',
                      help='Name of file in which are environments used in stimulation continuation.')

    pars.add_argument('-l', '--log_file', dest='log_file', action='store',
                      help='Name of file in which will be stored log information.')

    pars.add_argument('-v', '--verbose', dest='verbose', action='count',
                      help='Increase verbosity level. (-v = INFO; -vv = DEBUG) '
                           'Default: WARNING level')


def set_logging_options():
    # Setting log_level and log file whether specified.
    log_level = logging.WARNING

    if args.verbose == 1:
        log_level = logging.INFO

    elif args.verbose >= 2:
        log_level = logging.DEBUG
    # Set up basic configuration, out to std err with a reasonable default format.
    if args.log_file is not None:
        logging.basicConfig(filename=args.log_file, level=log_level)
    else:
        logging.basicConfig(level=log_level)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program is implementation of Steels simulation.")
    add_arguments(parser)
    args = parser.parse_args()

    set_logging_options()

    # Check whether start new simulation or continue old.
    start_simulation = args.simulation_file
    continue_simulation = args.load_simulation

    # Start new simulation.
    params = Parser().parse_simulation(args.simulation_file)
    params["dump_often"] = args.dump
    # Main part - running steels experiment.

    results, simulation = steels_experiment(**params)

    # Saving results of simulation - always.
    with open(args.results_file, "w") as f:
        cPickle.dump((results, params), f)

    # Saving whole simulation - only when specified.
    save_simulation = args.save_simulation
    if save_simulation is not None:
        with open(save_simulation, 'w') as f:
            cPickle.dump((simulation, params), f)
