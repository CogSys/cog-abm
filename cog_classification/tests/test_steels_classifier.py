from sklearn import datasets

from cog_classification.steels.steels_classifier import SteelsClassifier


class TestSteelsClassifier:

    def __init__(self):
        self.classifier = None

    def setup(self):
        self.classifier = SteelsClassifier()

    def test_classifier_1(self):
        """ Simple test using irises. """
        iris = datasets.load_iris()
        self.classifier.fit(iris.data, iris.target)

        success = 0
        for i, sample in enumerate(iris.data):
            success += self.classifier.predict([sample]) == iris.target[i]

        print(float(success)/len(iris.data))

    def test_classifier_2(self):
        """ Simple test using easy learning data. """
        self.classifier.fit([[1], [2], [3], [4]], [1, 2, 3, 4])

        success = 0
        for i in range(1, 5):
            success += self.classifier.predict([[i]]) == [i]

        print(float(success)/4)
