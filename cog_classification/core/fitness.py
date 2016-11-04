from collections import deque


class Fitness:
    """
    Accumulates information about agent fitness.
    """

    def __init__(self):
        pass

    def get_measure(self):
        """
        Exports information about agent fitness.
        """
        pass

    def update(self, value):
        """
        Adds new information about agent fitness.

        :param value: the new information about agent fitness.
        """
        pass


class StandardFitness(Fitness):
    """
    Monitors total win rate of agent.
    """

    def __init__(self):
        Fitness.__init__(self)
        self.success = 0
        self.all = 0

    def get_measure(self):
        """
        :return: total win rate of agent.
        :rtype: float
        """

        if self.all == 0:
            return 0
        else:
            return float(self.success) / self.all

    def update(self, value):
        """
        :param value: the information about success or loss of agent.
        :type value: bool
        """
        self.all += 1
        self.success += value


class CurrentFitness(Fitness):
    """
    Monitors current win rate of agent.

    :param long scope: on how many last games the win rate will be calculated?
    """

    def __init__(self, scope=50):
        Fitness.__init__(self)
        self.scope = scope
        self.memories = deque([])

    def get_measure(self):
        """
        :return: current win rate of agent.
        :rtype: float
        """
        if len(self.memories) < 1:
            return 0
        else:
            return float(sum(self.memories)) / len(self.memories)

    def update(self, value):
        """
        :param value: the information about success or loss of agent.
        :type value: bool
        """
        while len(self.memories) >= self.scope:
            self.memories.pop()
        self.memories.append(value)
