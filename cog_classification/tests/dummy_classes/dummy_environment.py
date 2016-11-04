from cog_classification.core.environment import Environment

import numpy as np


class DummyEnvironment(Environment):

    def __init__(self):
        samples = []
        classes = []
        for i in range(10):
            for j in range(10):
                samples.append([10 * i + j])
                classes.append(i)
        Environment.__init__(self, np.array(samples), np.array(classes))

