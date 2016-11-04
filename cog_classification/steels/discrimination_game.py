class DiscriminationGame:
    """
    This class implements steels discrimination game.

    :param long samples_number: the number of samples shown to agent in one interaction including topic. \
        Value from 2 to infinity.
    :param float good_agent_measure: the threshold which affects generation of new categories. \
        Value from (as rarely as possible) to 1 (always).

    Discrimination game was described in Luc Steels and Tony Belpaeme
    "Coordinating perceptually grounded categories through language: A case study for colour".
    """

    def __init__(self, samples_number=4, good_agent_measure=0.95):
        assert samples_number > 1
        self.samples_number = samples_number

        assert good_agent_measure >= 0
        assert good_agent_measure <= 1
        self.good_agent_measure = good_agent_measure

    def interact(self, agents, environment):
        """
        One turn of interaction in discrimination game.

        :param Network agents: source of agents for discrimination game.
        :param Environment environment: source of stimuli for discrimination game.
        """
        agent = agents.get_agent()
        (result, topic_category), topic_index = self.play(agent, environment)
        self.learning_after_game(agent, topic_index, environment, topic_category, result)
        agent.forget()
        agent.update_fitness_measure("DG", result)

    def learning_after_game(self, agent, topic_index, environment, topic_category, result):
        """
        Changes given agent state depending on result.

        :param Agent agent: the agent whose state will be changed.
        :param long topic_index: index of topic in environment.
        :param Environment environment: the environment from which topic origins.
        :param hashable topic_category: the category of topic.
        :param bool result: the result of the game: True - success, False - failure.
        """

        if result:
            agent.increase_weights_sample_category(topic_index, environment, topic_category)

        elif agent.get_fitness_measure("DG") >= self.good_agent_measure:
            return agent.add_sample(topic_index, environment, topic_category), topic_index

        else:
            return agent.add_sample(topic_index, environment), topic_index

    def play(self, agent, environment):
        """
        The core implementation of single game without changing agent.

        :param Agent agent: the agents that plays the game.
        :param Environment environment: the environment form which origins all games stimuli.

        SteelsAgent gets sets of samples in which one is chosen as topic.

        SteelsAgent task is to classify this topic as different from other samples.
        """
        topic_index = environment.get_random_sample_index()
        topic_class = environment.get_class(topic_index)
        other_samples = [self.sample_from_other_class(topic_class, environment) for _ in range(self.samples_number - 1)]

        topic = environment.get_sample(topic_index)
        return self.play_with_given_samples(agent, topic, other_samples)

    @staticmethod
    def play_with_given_samples(agent, topic, other_samples):
        """
        The implementation of single game with given topic and other samples.

        :param Agent agent: the agents that plays the game.
        :param topic: the highlighted stimulus.
        :param list other_samples: stimuli from classes other than class of topic.

        :returns: * the result of the game. *(bool)*
            * the category that was chosen for topic. *(hashable)*
        """
        topic_category = agent.predict(topic)
        other_categories = [agent.predict(sample) for sample in other_samples]

        if topic_category is None:
            result = False
        else:
            result = topic_category not in other_categories

        return result, topic_category

    @staticmethod
    def sample_from_other_class(sample_class, environment):
        """
        Finds in environment sample that has different class than sample class.

        :param hashable sample_class: the prohibited class.
        :param Environment environment: the environment from which sample will be picked.

        :return: the sample that has class other than sample class.
        """
        while True:
            index, sample, taken_class = environment.get_random_sample()
            if not taken_class == sample_class:
                return sample
