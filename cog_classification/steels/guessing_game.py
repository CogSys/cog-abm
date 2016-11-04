import random
import numpy as np

from cog_classification.steels.discrimination_game import DiscriminationGame


class GuessingGame:
    """
    This class implements steels guessing game.

    :param long samples_number: the number of samples shown to agent in one interaction including topic. \
        Value from 2 to infinity.
    :param float good_agent_measure: the threshold which affects generation of new categories. Value from 0 to 1.
    :param string role_model: the way of assign agents to roles.\
        "RANDOM" - both agents has equal chance of becoming speaker. \
        "SPEAKER" - first agent always becomes speaker. \
        "HEARER" - first agent always becomes hearer.

    Guessing game was described in Luc Steels and Tony Belpaeme
    "Coordinating perceptually grounded categories through language: A case study for colour".
    """

    def __init__(self, samples_number=4, good_agent_measure=0.95, role_model="RANDOM"):
        self.samples_number = samples_number
        self.good_agent_measure = good_agent_measure
        self.role_model = role_model

        self.game = DiscriminationGame(samples_number, good_agent_measure)

    def interact(self, agents, environment):
        """
        One turn of interaction in guessing game.

        :param Network agents: source of agents for discrimination game.
        :param Environment environment: source of stimuli for discrimination game.
        """
        agents = agents.get_agents(2)

        # Assigning roles to agents.
        if self.role_model == "RANDOM":
            if random.randint(0, 1):
                speaker = agents[0]
                hearer = agents[1]
            else:
                speaker = agents[1]
                hearer = agents[0]
        elif self.role_model == "SPEAKER":
            speaker = agents[0]
            hearer = agents[1]
        elif self.role_model == "HEARER":
            speaker = agents[1]
            hearer = agents[0]
        else:
            raise ValueError

        # Choose of topic and other stimuli from environment.
        topic_index, topic, topic_class = environment.get_random_sample()
        other_samples = [DiscriminationGame.sample_from_other_class(topic_class, environment)
                         for _ in range(self.samples_number - 1)]

        # Speaker is trying to discriminate topic from other samples.
        result, speaker_category = self.game.play_with_given_samples(speaker, topic, other_samples)

        # If speaker can discriminate topic from other_samples.
        if result:
            # Speaker is looking for word that suits topic category.
            word = speaker.find_word_for_category(speaker_category)

            # Hearer is looking for category that suits speaker word.
            hearer_category = hearer.find_category_for_word(word)

            # If hearer finds such category.
            if hearer_category is not None:

                # The other samples and topic are shuffled to avoid position clue.
                all_samples = other_samples + [topic]
                random.shuffle(all_samples)

                # Hearer trying to guess topic that belongs the most to category.
                guessed_topic = hearer.the_best_sample_for_category(hearer_category, all_samples)

                # If hearer correctly assumed that topic belongs to guesses category the most.
                if np.array_equal(topic, guessed_topic):
                    result = "Success"

                # If hearer didn't assume that topic belongs to guesses category the most.
                else:
                    result = "Not matching samples."

            # If hearer doesn't find such category for word.
            else:
                result = "Hearer didn't know word."

        # If speaker cannot discriminate topic from other_samples.
        else:
            result = "Speaker failed discrimination."

        # Actions taken up depending on game results.
        if result == "Success":

            # Strengthen association between word and category.
            speaker.increase_weight_word_category(word, speaker_category)
            # Strengthen association between word and category.
            hearer.increase_weight_word_category(word, hearer_category)

            # Weaken associations between other categories and word.
            speaker.decrease_weights_for_other_categories(word, speaker_category)
            # Weaken associations between other words and category.
            hearer.decrease_weights_for_other_words(word, hearer_category)

            # Strengthen memory of category.
            speaker.increase_weights_sample_category(topic_index, environment, speaker_category)
            # Strengthen memory of category.
            hearer.increase_weights_sample_category(topic_index, environment, hearer_category)

            speaker.update_fitness_measure("GG", True)
            speaker.update_fitness_measure("DG", True)

            hearer.update_fitness_measure("GG", True)

            speaker.forget()
            hearer.forget()

        elif result == "Speaker failed discrimination.":
            # Speaker learns topic.
            self.game.learning_after_game(speaker, topic_index, environment, speaker_category, False)

            speaker.update_fitness_measure("GG", False)
            speaker.update_fitness_measure("DG", False)
            hearer.update_fitness_measure("GG", False)

            speaker.forget()

        elif result == "Hearer didn't know word.":
            # Hearer plays discrimination game.
            result, hearer_category = self.game.play_with_given_samples(hearer, environment.get_sample(topic_index),
                                                                        other_samples)
            # If hearer cannot discriminate topic.
            if not result:
                # Hearer learns topic.
                hearer_category, _ = self.game.learning_after_game(hearer, topic_index, environment, hearer_category, result)

            # If hearer cannot learn then crash.
            if hearer_category is None:
                raise ValueError

            # Associating the category for topic with word.
            hearer.add_word_to_category(word, hearer_category)

            speaker.update_fitness_measure("GG", False)
            speaker.update_fitness_measure("DG", True)
            hearer.update_fitness_measure("GG", False)
            hearer.update_fitness_measure("DG", result)

            speaker.forget()
            hearer.forget()

        elif result == "Not matching samples.":

            # Weaken association between word and category.
            speaker.decrease_weight_word_category(word, speaker_category)
            # Weaken association between word and category.
            hearer.decrease_weight_word_category(word, hearer_category)

            # Hearer learns topic.
            self.game.learning_after_game(hearer, topic_index, environment, hearer_category, result=False)

            speaker.update_fitness_measure("GG", False)
            speaker.update_fitness_measure("DG", True)
            hearer.update_fitness_measure("GG", False)

            speaker.forget()
            hearer.forget()
        else:
            raise ValueError
