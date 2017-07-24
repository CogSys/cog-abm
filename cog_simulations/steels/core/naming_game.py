import random
from cog_simulations.cog_abm.core.interaction import Interaction
from discrimination_game import DiscriminationGame


class NamingGame(Interaction):
    """
    Based mostly on work "Colourful language and colour categories"
    of Tony Belpaeme and Joris Bleys.
    """

    def __init__(self, disc_game=None, context_size=None, learning_mode=True, environment=None, game_name=None,
                 inc_category_threshold=0.95, agents=None, role_model="RANDOM"):

        if disc_game is None:

            disc_game_name = None
            if game_name:
                disc_game_name = "DG_%s" % game_name

            disc_game = DiscriminationGame(environment=environment, inc_category_threshold=inc_category_threshold,
                                           game_name=disc_game_name)
            if context_size is not None:
                disc_game.context_len = context_size

        self.disc_game = disc_game
        self.learning_mode = learning_mode
        self.environment = environment

        self.game_name = game_name or 'NG'
        self.agents = agents
        self.role_model = role_model

    def change_environment(self, environment):
        self.environment = environment
        self.disc_game.change_environment(environment)

    @staticmethod
    def num_agents():
        return 2

    def set_inc_category_threshold(self, new_inc_category_threshold):
        self.disc_game.set_inc_category_threshold(new_inc_category_threshold)

    def save_result(self, agent, result):
        agent.add_payoff(self.game_name, int(result))

    def name_game(self, speaker, hearer):
        """
        The most important method: the naming game logic.

        Each line explained by a comment.
        """

        # Get a random list of stimuli from environment of size self.disc_game.context_len:
        context = self.environment.get_stimuli(self.disc_game.context_len)

        # The first element of this context is topic:
        topic = context[0]
        s_category = tuple(topic.values)

        # word = word that speaker uses to call the topic.
        word = speaker.state.word_for(s_category)
        # If there is no word that speaker has for this category:
        if word is None and self.learning_mode:
            # A random word is chosen for this category and added:
            word = speaker.state.lexicon.add_element(s_category)

        # h_word_category = a category that hearer thinks of when using the word:
        h_word_category = hearer.state.category_for(word)

        # If there is no category for word in hearer's memory:
        if h_word_category is None:
            # The hearer learns a new word:
            if self.learning_mode:
                hearer.state.lexicon.add_element(s_category, word)
            return False

        # Checking game result: is the strongest activated stimulus same as topic?
        success = h_word_category == s_category

        # If it is the same:
        if success:
            """
            Increase the confidence in word for topic in both speaker and hearer:
            This is a symmetric function from the perspective of speaker and hearer:
            """
            # If agents can learn:
            if self.learning_mode:
                speaker.state.lexicon.inc_dec_categories(s_category, word)
                # ^^ as in 4.2 1.(a)
                hearer.state.lexicon.inc_dec_words(h_word_category, word)
                # ^^ as in 4.2 2.(a)
        # If it is different:
        else:
            """
            Decrease the confidence in word for topic in both speaker and hearer:
            Further, learning on hearer performed but without use of word.
            """
            # If agents can learn:
            if self.learning_mode:
                speaker.state.lexicon.decrease(s_category, word)
                # ^^ as in 4.2 1.(b)
                hearer.state.lexicon.decrease(h_word_category, word)
                # ^^ as in 4.2 2.(b)

        return success

    @staticmethod
    def find_best_matching_sample_to_category(agent, samples, category):
        max_reaction, max_sample = float("-inf"), None
        for sample in samples:
            strength = agent.state.sample_strength(category, agent.sense(sample))
            if strength > max_reaction:
                max_reaction, max_sample = strength, sample
        return max_sample

    def interact(self):

        agent1, agent2 = self.agents.get_two_agents()

        if self.role_model == "RANDOM":
            if random.randint(0, 1):
                speaker = agent1
                hearer = agent2
            else:
                speaker = agent2
                hearer = agent1
        elif self.role_model == "SPEAKER":
            speaker = agent1
            hearer = agent2
        elif self.role_model == "HEARER":
            speaker = agent2
            hearer = agent1
        else:
            raise ValueError

        r = self.name_game(speaker, hearer)
        self.save_result(speaker, r)
        self.save_result(hearer, r)
        return (self.game_name, r), (self.game_name, r)

    def __repr__(self):
        return "NamingGame: %s" % self.disc_game
