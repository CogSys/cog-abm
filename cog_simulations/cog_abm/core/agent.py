"""
Module implementing agent in our system
"""
from multiprocessing import Lock


class Agent(object):
    """
    Class representing agent in our system.

    In most cases you shouldn't change or redefine this class.
    There is special class for that: AgentState
    """
    AID = 0
    AID_lock = Lock()

    def __init__(self, aid=None, state=None, sensor=None):
        self.id = aid or Agent.get_next_id()
        self.sensor = sensor
        self.state = state
        self.inter_res = []
        self.fitness = {}

    @classmethod
    def get_next_id(cls):
        cls.AID_lock.acquire()
        w = cls.AID
        cls.AID += 1
        cls.AID_lock.release()
        return w

    def get_id(self):
        return self.id

    def set_state(self, state):
        self.state = state

    def set_sensor(self, sensor):
        self.sensor = sensor

    def set_fitness_measure(self, fitness_id, fitness):
        self.fitness[fitness_id] = fitness

    def get_fitness_measure(self, fitness_id):
        return self.fitness[fitness_id]

    def get_fitness(self, f_id):
        return self.fitness[f_id].get_fitness()

    def add_payoff(self, f_id, payoff, weight=1.):
        self.fitness[f_id].add_payoff(payoff, weight)

    def sense(self,  stimulus):
        """
        Returns list with sensors perception of given stimulus
        """
        return self.sensor.sense(stimulus)

    # 'sense' is in name to make clear what happens
    def sense_and_classify(self, stimulus):
        return self.state.classify(self.sense(stimulus))

    def sense_and_classify_p_val(self, stimulus):
        return self.state.classify_p_val(self.sense(stimulus))

    def sense_and_class_probabilities(self, stimulus):
        return self.state.class_probabilities(self.sense(stimulus))

    def __repr__(self):
        return "Agent(" + str(self.id) + ":" + str(self.state) + ")"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def add_inter_result(self, res):
        self.inter_res.append(res)
