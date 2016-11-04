import sys
sys.path.append('../')
import unittest
from cog_abm.ML.orange_wrapper import OrangeClassifier
from cog_abm.ML.core import NominalAttribute, NumericAttribute, Sample
import orange
from itertools import izip


class TestOrange(unittest.TestCase):

    def setUp(self):
        self.classifiers = [
            ("BayesLearner", [], {}),
            ("TreeLearner", [], {}),
            ("kNNLearner", [], {"k": 1}),
            ("kNNLearner", [], {"k": 3}),
            ("TreeLearner", [], {})
        ]
        self.knn1 = OrangeClassifier(self.classifiers[2][0])
        self.knn3 = OrangeClassifier(self.classifiers[3][0])
        self.tree = OrangeClassifier(self.classifiers[4][0])
        self.cls_meta = NominalAttribute([0, 1])
        self.meta = [NumericAttribute() for _ in xrange(3)]
        self.train_set = [
            Sample([0, 0, 0], self.meta, 0, self.cls_meta),
            Sample([0, 1, 0], self.meta, 0, self.cls_meta),
            Sample([0, 0, 1], self.meta, 0, self.cls_meta),
            Sample([3, 0, 0], self.meta, 1, self.cls_meta),
            Sample([3, 1, 0], self.meta, 1, self.cls_meta),
            Sample([3, 0, 1], self.meta, 1, self.cls_meta),
        ]

    def test_classifier_creation(self):
        """ Proper classifier creation """

        for (c, args, kargs) in self.classifiers:
            classifier = OrangeClassifier(c, *args, **kargs)
            self.assertEqual(getattr(orange, c),
                             type(classifier.classifier))

    def test_classification(self):

        classifier = self.knn1
#        classifier = self.tree
        classifier.train(self.train_set)
        expected = map(str, [0, 0, 0, 1, 1, 1, 0, 1])
        samples = [s for s in self.train_set]
        samples.extend([Sample([1, 0, 0], self.meta), Sample([2, 1, 0], self.meta)])
        for e, s in izip(expected, samples):
            self.assertEqual(e, classifier.predict(s))
            k, p = classifier.classify_p_val(s)
            self.assertTrue(0. <= p <= 1.)
            self.assertEqual(k, classifier.predict(s))
            p2 = classifier.class_probabilities(s)
            self.assertAlmostEqual(1., sum(p2.values()), delta=0.00001)

    def test_weighted_training(self):
        samples_with_weights = \
            [(s, float(i == 0)) for i, s in enumerate(self.train_set)]
        classifier = self.knn1
        test_sample = self.train_set[-1]
        classifier.train(self.train_set)
        self.assertEqual('1', classifier.predict(test_sample))
        classifier.train_with_weights(samples_with_weights)
        self.assertEqual('0', classifier.predict(test_sample))
