# class SteelsAgentState(AgentState):
class SteelsAgentState(object):

    def __init__(self, classifier):
        self.classifier = classifier

    def classify(self, sample):
        return self.classifier.classify(sample)

    def classify_p_val(self, sample):
        return self.classifier.classify_p_val(sample)

    def class_probabilities(self, sample):
        return self.classifier.class_probabilities(sample)

    def sample_strength(self, category, sample):
        return self.classifier.sample_strength(category, sample)
