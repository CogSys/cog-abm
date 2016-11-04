class Condition:
    """ Class wrapping condition of experiment end. """

    def __init__(self):
        pass

    def end(self, simulation):
        """ Test whether simulation parameters are suitable for simulation end. """
        pass

    def update(self, condition):
        """ Changes behavior of self depending on condition. """
        pass


class IterationCondition(Condition):
    """
    Class implementing plain stop iteration.

    :param long max_iterations: number of last iteration before stop. Value from 1 to infinite.
    """

    def __init__(self, max_iterations):
        Condition.__init__(self)
        assert max_iterations > 0
        self.max_iterations = max_iterations

    def end(self, simulation):
        """
        Test whether simulation iteration number is suitable for simulation end.

        :param Simulation simulation: The tested simulation.

        :return: Whether simulation should end.
        :rtype: bool
        """
        return simulation.iteration >= self.max_iterations

    def update(self, condition):
        """
        Increase self max_iterations by condition max_iterations number.

        :param IterationCondition condition: the condition which max_iteration will increase self max_iterations.
        """
        self.max_iterations += condition.max_iterations
