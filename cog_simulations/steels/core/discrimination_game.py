from cog_simulations.steels.metrics import success_of_agent
from cog_simulations.cog_abm.core.interaction import Interaction

import random


class DiscriminationGame(Interaction):

    def __init__(self, context_len=4, inc_category_threshold=0.95, environment=None, game_name=None, agents=None):
        self.context_len = context_len
        self.inc_category_threshold = inc_category_threshold
        self.environment = environment
        self.game_name = game_name or "DG"
        self.agents = agents

    def change_environment(self, environment):
        self.environment = environment

    @staticmethod
    def num_agents():
        return 2

    def set_inc_category_threshold(self, new_inc_category_threshold):
        self.inc_category_threshold = new_inc_category_threshold

    def save_result(self, agent, result):
        agent.add_payoff(self.game_name, int(result))

    @staticmethod
    def disc_game(agent, context, topic):
        """
        Checking whether agent can discriminate topic from context.
        Topic is element of context.
        """
        c_topic = agent.sense_and_classify(topic)
        # No problem if c_topic is None => count>1 so it will add new category.

        c_context = [agent.sense_and_classify(c) for c in context]
        count = c_context.count(c_topic)
        return count == 1, c_topic

    def learning_after(self, agent, topic, success, c_topic=None):
        success_rate = success_of_agent(agent, self.game_name)
        sensed_topic = agent.sense(topic)

        if success:
            agent.state.classifier.increase_samples_category(sensed_topic)
        elif success_rate >= self.inc_category_threshold:
            if c_topic is None:
                c_topic = agent.state.classifier.classify(sensed_topic)
            agent.state.classifier.add_category(sensed_topic, c_topic)
        else:
            agent.state.classifier.add_category(sensed_topic)

        # Lower strength of memory.
        agent.state.classifier.forgetting()

    def play_with_learning(self, agent, context, topic):
        success, c_topic = self.disc_game(agent, context, topic)
        self.learning_after(agent, topic, success, c_topic)
        return success, c_topic, topic, context

    def play_save(self, agent, context, topic):
        success, c_topic = self.disc_game(agent, context, topic)
        self.save_result(agent, success)
        return success, c_topic

    def play_learn_save(self, agent, context, topic):
        success, c_topic, topic, context = self.play_with_learning(agent, context, topic)
        self.save_result(agent, success)
        return success, c_topic, topic, context

    def get_setup(self):
        context = self.environment.get_stimuli(self.context_len)
        topic = context[0]
        # ^^^^ They are already shuffled - and needed when different classes.
        return context, topic

    def interact_one_agent(self, context=None, topic=None):
        if context is None or topic is None:
            context, topic = self.get_setup()
        agent = random.choice(self.agents.agents)
        success, _, _, _ = self.play_with_learning(agent, context, topic)
        self.save_result(agent, success)
        return success

    def interact(self):

        agent1, agent2 = self.agents.get_two_agents()
        context, topic = self.get_setup()
        return (
            (self.game_name, self.interact_one_agent(agent1, context, topic)),
            (self.game_name, self.interact_one_agent(agent2, context, topic))
        )

    def __repr__(self):
        return "DiscriminationGame: context_len=%s;" \
               " inc_category_threshold=%s" % \
               (self.context_len, self.inc_category_threshold)
