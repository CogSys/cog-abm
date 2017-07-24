"""
This module implements Steels experiment.
"""
import logging

from cog_simulations.cog_abm.core import Simulation
from reactive_unit import ReactiveUnit
from adaptative_network import AdaptiveNetwork
from steels_classifier import SteelsClassifier


log = logging.getLogger('steels')
log.level = logging.INFO


# Steels experiment main part
def steels_experiment(num_iter=1000, dump_freq=50, alpha=0.1, beta=1, sigma=10, agents=None,
                      interactions_sets=None, dump_often=None,
                      num_agents=None):
    # Don't remove num_agents it is required in experiment continuation,
    """
    An experiment in which topology, type and learning can change after some number of iterations.
    """

    games_labels = load_games_labels(interactions_sets)
    agents = load_agents(agents, games_labels)

    for interactions_set in interactions_sets.values():
        for interaction_data in interactions_set:
            for agent in agents:
                interaction_data["agents"].add_agent(agent)

    interactions_sets, colour_order = load_interactions_sets(interactions_sets)

    AdaptiveNetwork.def_alpha = float(alpha)
    AdaptiveNetwork.def_beta = float(beta)
    ReactiveUnit.def_sigma = float(sigma)

    log.info("Running steels experiment with: %s",
             str({'num agents': len(agents)}))

    s = Simulation(interactions_sets=interactions_sets, colour_order=colour_order, dump_often=dump_often)
    res = s.run(num_iter, dump_freq)

    return res, s


def load_games_labels(interactions_sets):
    labels = ["DG", "GG", "NG"]

    for interactions_set in interactions_sets.values():
        for interaction_data in interactions_set:
            if "game_name" in interaction_data:
                labels.append(interaction_data["game_name"])
                if interaction_data["type"] == "GuessingGame":
                    labels.append("DG_%s" % interaction_data["game_name"])

    return list(set(labels))


def load_agents(agents, games_labels):
    from cog_simulations.cog_abm.core.agent import Agent
    from cog_simulations.steels.core.steels_agent_state_with_lexicon import SteelsAgentStateWithLexicon
    from cog_simulations.cog_abm.agent.sensor import SimpleSensor
    from cog_simulations.steels import metrics
    from cog_simulations.cog_abm.extras.tools import def_value

    classifier, classifier_arg = SteelsClassifier, []
    classifier_arg = def_value(classifier_arg, [])

    true_agents = []
    for _ in agents:
        state = SteelsAgentStateWithLexicon(classifier(*classifier_arg))
        true_agent = Agent(state=state, sensor=SimpleSensor())

        for label in games_labels:
            true_agent.set_fitness_measure(label, metrics.get_cs_fitness())

        true_agents.append(true_agent)

    return true_agents


def load_interactions_sets(interactions_sets):
    from discrimination_game import DiscriminationGame
    from guessing_game import GuessingGame
    from naming_game import NamingGame

    from cog_simulations.cog_abm.extras.color import Color
    from cog_simulations.cog_abm.extras.extract_colour_order import extract_colour_order
    from cog_simulations.cog_abm.core.environment import Environment, RandomStimuliChooser

    general_colour_order = None

    new_interactions_sets = {}
    for start, interactions_set in interactions_sets.iteritems():
        new_interactions_set = []
        for interaction_data in interactions_set:
            context_size = interaction_data["context_size"]
            learning = interaction_data["learning"]
            inc_category_threshold = interaction_data["inc_category_threshold"]

            game_name = None
            if "game_name" in interaction_data:
                game_name = interaction_data["game_name"]

            role_model = "RANDOM"
            if "role_model" in interaction_data:
                role_model = interaction_data["role_model"]

            if interaction_data["type"] == "GuessingGame":
                interaction = GuessingGame(learning_mode=learning, game_name=game_name, role_model=role_model,
                                           agents=interaction_data["agents"])
            elif interaction_data["type"] == "NamingGame":
                interaction = NamingGame(learning_mode=learning, game_name=game_name, role_model=role_model,
                                         agents=interaction_data["agents"])
            else:
                interaction = DiscriminationGame(context_size, float(inc_category_threshold), game_name=game_name,
                                                 agents=interaction_data["agents"])

            environment = interaction_data["environment"]
            list_of_stimuli = []

            for stimulus in environment["source"]["stimuli"]:
                l = stimulus["L"]
                a = stimulus["a"]
                b = stimulus["b"]
                list_of_stimuli.append(Color(l, a, b))

            if "distance" in environment:
                dist = environment["distance"]
                chooser = RandomStimuliChooser(use_distance=True, distance=dist)
            else:
                chooser = RandomStimuliChooser()

            colour_order = None
            if "word_naming_per_color" in environment:
                word_naming_per_color = environment["word_naming_per_color"]
                colour_order = extract_colour_order(list_of_stimuli, word_naming_per_color)
                general_colour_order = colour_order

            env = Environment(list_of_stimuli, chooser, colour_order)
            interaction.change_environment(env)

            new_interactions_set.append(interaction)

        new_interactions_sets[start] = new_interactions_set

    return new_interactions_sets, general_colour_order
