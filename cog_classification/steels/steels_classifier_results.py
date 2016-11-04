from cog_classification.core.result import Result


class SteelsClassifierResults(Result):
    """
    Set of agents which have taken part in steels simulation.

    They can serves as classifier.
    """

    def __init__(self):
        Result.__init__(self)

    def save(self, simulation):
        """
        Save agents if it is the last iteration of simulation.

        :param Simulation simulation: simulation whose agents will be saved.
        """
        if simulation.end_condition.end(simulation):
            self.results['agents'] = simulation.agents.get_all_agents()

    def predict(self, samples):
        """
        Predicts classes of samples based on voting of agents.

        :param list samples: the samples which classes are predicted.

        :return: predicted classes of sample.
        :rtype: list
        """
        predicted_classes = []

        for sample in samples:
            classes_voting = {}

            for agent in self.results['agents']:
                prediction = agent.predict(sample)
                if prediction is not None:
                    class_vote = int(agent.get_category_class(prediction))
                    if class_vote in classes_voting:
                        classes_voting[class_vote] += 1
                    else:
                        classes_voting[class_vote] = 1

            best_class = None
            most_votes = 0

            for class_vote, number in classes_voting.iteritems():
                if number > most_votes:
                    most_votes = number
                    best_class = class_vote

            predicted_classes.append(best_class)

        return predicted_classes
