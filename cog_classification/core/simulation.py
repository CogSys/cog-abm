class Simulation:
    """ This class represents general logic of multi-agent simulation. """

    def __init__(self, agents, interactions, environment, result, end_condition):
        """
        :param Network agents: source of agents.
        :param BehaviorSwitcher interactions: source of interactions for agents.
        :param BehaviorSwitcher environment: source of samples for interactions.
        :param Result result: object that will accumulate statistics of simulation.
        :param Condition end_condition: object that determines end of simulation.
        """

        self.agents = agents
        self.interactions = interactions
        self.environment = environment
        self.result = result
        self.end_condition = end_condition

        self.iteration = 0

    def run(self):
        """
        Starts simulation.

        Returns:
            (Result) result of simulation.
        """
        self.result.save(self)

        # Main loop of simulation.
        while not self.end_condition.end(self):
            self.iteration += 1

            self.interactions.change(self.iteration)
            self.agents.change(self.iteration)
            self.environment.change(self.iteration)

            interaction = self.interactions.current_behavior
            environment = self.environment.current_behavior

            interaction.interact(self.agents, environment)

            self.result.save(self)

        return self.result

    def continue_simulation(self, agents=None, interactions=None, environment=None, end_condition=None):
        """
        Starts completed simulation from termination point with additional parameters.

        Args:
            like in __init__.

        Returns:
            (Result) result of whole simulation - form start of original simulation to the end of extended simulation.
        """
        self.agents.update(agents, self.iteration)
        self.interactions.update(interactions, self.iteration)
        self.environment.update(environment, self.iteration)
        self.end_condition.update(end_condition, self.iteration)

        return self.run()
