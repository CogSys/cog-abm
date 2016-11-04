"""
This module implements measurements used in evaluating the outcome of the
experiment.
"""
import math
import numpy

from itertools import combinations, imap

import sys
sys.path.append("../../")
sys.path.append("../")
sys.path.append(".")

from cog_simulations.cog_abm.extras.fitness import get_buffered_average

WINDOW_SIZE = 50


def get_ds_fitness():
    return get_buffered_average(WINDOW_SIZE)


def get_cs_fitness():
    return get_buffered_average(WINDOW_SIZE)


def discrimination_success_of_agent(agent):
    return agent.get_fitness("DG")


def discrimination_success_of_population(agents, iteration):
    if iteration == 0:
        return 0
    return numpy.mean([discrimination_success_of_agent(agent) for agent in agents])


def communication_success_of_agent(agent):
    return agent.get_fitness("GG")


def communication_success_of_population(agents, iteration):
    if iteration == 0:
        return 0
    return numpy.mean([communication_success_of_agent(agent) for agent in agents])


def success_of_agent(agent, fitness):
    return agent.get_fitness(fitness)


def success_of_population(agents, iteration, fitness):
    if iteration == 0:
        return 0
    return numpy.mean([success_of_agent(agent, fitness) for agent in agents])

# Calculate total variance of categories for the list of agents. This measure is sensitive to the number of categories.
def category_variance(agents, iteration):
    if iteration == 0:
        return 0
    # Taking category variance for every pair without repetition.
    total_variance = numpy.sum([category_variance_between_agents(pair) for pair in combinations(agents, 2)])
    n = len(agents)
    return (2 * total_variance) / (n * (n - 1))


# Calculate total variance of categories for the pair of agents.
def category_variance_between_agents(pair):
    agent1, agent2 = pair
    cat1 = agent1.state.classifier.categories
    cat2 = agent2.state.classifier.categories

    # For every category in cat1 and cat2 (dictionaries of categories)
    # we are taking a distance to closest category from other set.
    variance = numpy.sum([min([category_distance(cat1[c1], cat2[c2]) for c2 in cat2]) for c1 in cat1]) \
        + numpy.sum([min([category_distance(cat1[c1], cat2[c2]) for c1 in cat1]) for c2 in cat2])

    return variance / (len(cat1) * len(cat2))


# Calculate distance between two adaptive networks (categories).
def category_distance(c1, c2):
    reactive_units1 = c1.units
    reactive_units2 = c2.units

    # For every central value in reactive_units1 and reactive_units2 (list of values)
    # we are taking a distance to closest value from other set.

    distance = numpy.sum([min([value_distance(v1, v2) for v2 in reactive_units2]) for v1 in reactive_units1]) \
        + numpy.sum([min([value_distance(v1, v2) for v1 in reactive_units1]) for v2 in reactive_units2])

    return distance / (len(reactive_units1) * len(reactive_units2))


# Calculate distance between two reactive units (values).
def value_distance(r1, r2):
    (value1, weight1) = r1
    (value2, weight2) = r2

    return (weight1 * weight2) * value1.central_value.distance(value2.central_value)


def count_category_words(agents, parameters):

    def agent_words(agent):
        agents_words = set()
        stimuli = [unit.central_value
                   for adaptive_network in agent.state.classifier.categories.values()
                   for unit, _ in adaptive_network.units]
        for s in stimuli:
            agents_words.add(agent.state.word_for(
                agent.sense_and_classify(s)))
        return agents_words

    categories_nums = []
    words = set()
    for agent in agents:
        awords = agent_words(agent)
        words = words.union(awords)
        categories_nums.append(len(awords))

    return categories_nums + [len(words)]

def ds_a(agent):
    return agent.get_fitness("DG")


def ds(agents, it):
    if it == 0:
        return 0
    return math.fsum(imap(ds_a, agents)) / len(agents)


def cs_a(agent):
    return agent.get_fitness("GG")


def cs(agents, it):
    if it == 0:
        return 0
    return math.fsum(imap(cs_a, agents)) / len(agents)


def ru_dist(ru1, ru2):
    # print math.log(ru1[1], 0.8), math.log(ru2[1], 0.8)
    # return math.log(ru1[1], 0.001)*math.log(ru2[1], 0.001)*ru1[0].dist(ru2[0])
    # return ru1[1]*ru2[1]*ru1[0].dist(ru2[0])
    # what was in Steels:
    return ru1[0].dist(ru2[0])


def d(list_a, list_b, m):

    s1 = math.fsum([min([m(a, b) for b in list_b]) for a in list_a])
    s2 = math.fsum([min([m(a, b) for a in list_a]) for b in list_b])

    return (s1 + s2) / (len(list_a) * len(list_b))
    # /math.log((len(A) * len(B))+1)


# c & cp are lists of (ReactiveUnit, weight)
def d_category(c, cp):
    return d(c, cp, ru_dist)


# normally there would be agents
# a & ap are lists of lists of (ReactiveUnit, weight) - each inner list represents one adaptive network
def D(a, ap):
    return d(a, ap, d_category)


def cv(agents, it):
    if it == 0:
        return None  # it's fine on graph

#       ag_centres = [tuple(
#                           [tuple(
#                                                       [wru for wru in an.units])
#                                               for _, an in a.state.classifier.categories.iteritems()]
#                               ) for a in agents]
#       ag_centres = tuple(ag_centres)
    ag_centres = [[[wru for wru in an.units] for _, an in a.state.classifier.categories.iteritems()]
                  for a in agents]

    sum_d = math.fsum(D(a1, a2) for a1, a2 in combinations(ag_centres, 2) if len(a1) > 0 and len(a2) > 0)
    # return sum_d
    # return sum_d*2/(len(agents) * (len(agents)-1))
    return sum_d*2/(len(agents) * (len(agents)-1))
#       return (len(agents) * (len(agents)-1))/(sum_d*2)


def mcv(agents_centres):
    """ calculates the category variance between agents categorical split
    @agents_centres: list of lists of centre value = list of classes:
            e.g.: [[c1, c2, c3], [c1, c2], [c1], [c1, c2, c3, c4]]
    @return: number denoting the variance value
    """
    cat_var = 0.
    for i in range(1, len(agents_centres)):
        for j in range(i):
            cat_var += cat_dist(agents_centres[i], agents_centres[j])
    cat_var /= len(agents_centres) * (len(agents_centres) - 1)
    cat_var *= 2
    return cat_var


def cv_prim(agents_centres1, agents_centres2):
    """ calculates the category varianve between agents categorical split
    @agents_centres1: list of lists of centre value:
            e.g.: [[c1, c2, c3], [c1, c2], [c1], [c1, c2, c3, c4]]
    @agents_centres2: list of lists of centre value:
            e.g.: [[c1, c2, c3], [c1, c2], [c1], [c1, c2, c3, c4]]
    @return: number denoting the variance value
    """
    cat_var = math.fsum([cat_dist(center1, center2) for center1 in
                        agents_centres1 for center2 in agents_centres2])
    cat_var /= len(agents_centres1) * (len(agents_centres2))
    return cat_var


def cat_dist(set1, set2):
    """ returns distance between 2 given sets
    """
    sum1 = 0.
    for e1 in set1:
        h1 = min(basic_dist(e1, e2) for e2 in set2)
        sum1 += h1

    sum2 = 0
    for e2 in set2:
        h2 = min(basic_dist(e2, e1) for e1 in set1)
        sum2 += h2
    return 1.0 * (sum1 + sum2) / (len(set1) * len(set2))


def basic_dist(set1, set2):
    """
    """
    return math.sqrt(sum((e1 - e2)**2
                     for e1, e2 in zip(set1, set2)))


if __name__ == '__main__':
    # To test some new distances - should use weights!
    from core.reactive_unit import ReactiveUnit
    rus = [(ReactiveUnit([x, x, x]), 1./(x+1)) for x in xrange(3)]
    rus2 = [(ReactiveUnit([x+1, x+1, x+1]), 1./(x+1)) for x in xrange(3)]
    print rus
    print rus2
    print d_category(rus, rus2)
    rus = [(ReactiveUnit([x, x, x]), 1.) for x in xrange(3)]
    rus2 = [(ReactiveUnit([x+20, x-19, x+18]), 1.) for x in xrange(3)]
    print d_category(rus, rus2)
