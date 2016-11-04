class Result:
    """
    Class that collects results of simulation.
    """

    def __init__(self):
        self.results = {}

    def save(self, simulation):
        """
        Save results of simulation.

        :param Simulation simulation: the simulation that will be saved.
        """
        pass

    def get_results(self):
        """
        :return: all saved results.
        :rtype: dictionary
        """
        return self.results


class StandardResult(Result):
    """
    Class that saves all agents statistics every given time.

    :param long gap: how often results will be saved.
    """

    def __init__(self, gap=50):
        Result.__init__(self)
        self.gap = gap

    def save(self, simulation):
        """
        Saves all agents fitness measures if simulation's iteration number is divided by gap.

        :param Simulation simulation: the simulation that will be saved.
        """
        iteration = simulation.iteration

        if iteration % self.gap == 0:

            results = {"iteration": iteration}

            for agent in simulation.agents.get_all_agents():
                for fitness_name in agent.get_fitness_measures():

                    fitness_measure = agent.get_fitness_measure(fitness_name)

                    if fitness_name in results:
                        results[fitness_name].append(fitness_measure)
                    else:
                        results[fitness_name] = [fitness_measure]

            self.results[iteration / self.gap] = results


class ResultsContainer(Result):
    """
    Class that can contains other results and gather all of them at the same time.

    :param dictionary results: dictionary of gathered results with their names as keys.
    """

    def __init__(self, results):
        Result.__init__(self)
        self.results = results

    def save(self, simulation):
        """
        Saves all containing results.

        :param Simulation simulation: the simulation that will be saved.
        """

        for result in self.results.values():
            result.save(simulation)

    def get_results(self):
        """
        :return: all saved results.
        :rtype: dictionary
        """
        results = {}

        for name, results in self.results.iteritems():
            results[name] = results.get_results()

        return results
