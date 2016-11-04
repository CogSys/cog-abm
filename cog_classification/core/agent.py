from multiprocessing import Lock


class Agent:
    """
    Class representing agent in the system.

    :param hashable aid: agent id. Unique identifier of agent.

    Agent can have fitness measures which value can be updated and read.
    """

    # AID is set that it will match networks nodes.
    AID = 0
    AID_lock = Lock()

    def __init__(self, aid=None):
        self.id = aid or Agent.get_next_id()

        # Fitness is dictionary of agent's fitness measures.
        self.fitness = {}

    @classmethod
    def get_next_id(cls):
        """
        Generates new unique id for agent.

        | It asserts that user doesn't specify id value for any agent.
        | Range of id numbers is from 0 to infinity.
        """
        cls.AID_lock.acquire()
        aid = cls.AID
        cls.AID += 1
        cls.AID_lock.release()
        return aid

    def get_fitness_measure(self, name):
        """
        :param hashable name: name of fitness measure.
        :return: value of fitness measure with a specific name.
        """
        return self.fitness[name].get_measure()

    def get_fitness_measures(self):
        """
        :return: names of all fitness measures.
        :rtype: list of hashable
        """
        return self.fitness.keys()

    def set_fitness(self, name, fitness_measure):
        """
        Adds to agent given fitness measure with a specific name.

        :param hashable name: name of fitness measure.
        :param fitness fitness_measure: the fitness measure that will be used by agent.
        """
        self.fitness[name] = fitness_measure

    def update_fitness_measure(self, name, information):
        """
        Gives information to fitness measure with a specific name.

        :param hashable name: name of fitness measure.
        :param information: information given to fitness measure.
        """
        self.fitness[name].update(information)
