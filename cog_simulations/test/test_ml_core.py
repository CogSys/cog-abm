import math
import random
import unittest

from cog_abm.ML.core import (NominalAttribute,
    NumericAttribute, Sample, load_samples_arff,
    split_data, split_data_cv, normalize_samples)


animals = ["dog", "cat", "lion", "duck", "python:)"]


class TestAttributes(unittest.TestCase):

    def setUp(self):
        self.symbols = animals
        self.na = NominalAttribute(self.symbols)

    def test_numeric_attr_getting_value(self):
        na = NumericAttribute()
        for i in xrange(10):
            self.assertEqual(i, na.get_value(i))

    def test_nominal_attr_getting_value(self):
        na = NominalAttribute(self.symbols)
        for i, s in enumerate(self.symbols):
            self.assertEqual(s, na.get_value(i))
            self.assertEqual(s, na.get_symbol(i))
            self.assertEqual(i, na.get_idx(s))

    def test_equality(self):
        self.assertEqual(self.na, NominalAttribute(animals))
        self.assertEqual(self.na,
                NominalAttribute(["dog", "cat", "lion", "duck", "python:)"]))
        self.assertNotEqual(self.na, NominalAttribute(animals + ["donkey"]))
        self.assertEqual(NumericAttribute(), NumericAttribute())
        self.assertNotEqual(self.na, NumericAttribute())


class TestSample(unittest.TestCase):

    def setUp(self):
        self.meta = [NumericAttribute(), NominalAttribute(animals)]
        self.sample = Sample([1.2, self.meta[1].get_idx("dog")], self.meta)
        self.meta_cl = NominalAttribute(animals)
        self.sample_cl = Sample([100, self.meta[1].get_idx("cat")], self.meta,
                                self.meta_cl.get_idx("duck"), self.meta_cl)

    def test_basic(self):
        self.assertIsNone(self.sample.get_cls())
        self.assertEqual(self.sample_cl.get_cls(), "duck")

        self.assertEqual(self.sample.get_values(), [1.2, "dog"])
        self.assertEqual(self.sample_cl.get_values(), [100, "cat"])

    def test_equality(self):
        self.assertNotEqual(self.sample, self.sample_cl)

        meta = [NumericAttribute(), NominalAttribute(animals)]
        sample = Sample([1.2, meta[1].get_idx("dog")], meta)
        self.assertEqual(self.sample, sample)
        self.assertNotEqual(self.sample, self.sample_cl)
        meta = [NumericAttribute(), NominalAttribute(animals), NumericAttribute()]
        sample = Sample([1.2, meta[1].get_idx("dog"), 3.14], meta)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)

        meta = [NumericAttribute(), NominalAttribute(animals)]
        sample = Sample([1.2, meta[1].get_idx("cat")], meta)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)

        sample = Sample([1.3, meta[1].get_idx("dog")], meta)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)

        sample = Sample([100, self.meta[1].get_idx("cat")], self.meta,
                                self.meta_cl.get_idx("duck"), self.meta_cl)
        self.assertEqual(self.sample_cl, sample)
        self.assertNotEqual(self.sample, sample)

        sample = Sample([10.20, self.meta[1].get_idx("cat")], self.meta,
                                self.meta_cl.get_idx("duck"), self.meta_cl)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)


class TestSampleDistances(unittest.TestCase):
    pass


class TestSampleNormalization(unittest.TestCase):

    def _gen_samples(self):
        na = self.meta[-1]
        return [
            Sample([0., 0., na.get_idx('dog')], self.meta),
            Sample([-100., 30., na.get_idx('lion')], self.meta),
            Sample([50, -20., na.get_idx('cat')], self.meta),
            Sample([2, -6, na.get_idx('dog')], self.meta),
        ]

    def setUp(self):
        self.meta = [NumericAttribute(), NumericAttribute(),
            NominalAttribute(animals)]
        self.samples = self._gen_samples()
        self.samples_org = self._gen_samples()

    def testSampleNormalization(self):
        samples_config = normalize_samples(self.samples)
        ss, ssorg = self.samples, self.samples_org
        self.assertEqual(samples_config, [150., 50., None])
        self.assertEqual(ss[0], ssorg[0])
        for s1, s2 in zip(ss, ssorg)[1:]:
            self.assertNotEqual(s1, s2)
            s1v, s2v = s1.get_values(), s2.get_values()
            self.assertNotEqual(s1v[0], s2v[0])
            self.assertNotEqual(s1v[1], s2v[1])
            self.assertEqual(s1v[2], s2v[2])

    def testAnotherDistance(self):
        normalize_samples(self.samples)
        ss = self.samples
        for s1 in ss:
            for s2 in ss:
                self.assertTrue(0. <= s1.distance(s2)
                     <= 1. * len(s1.values))


class TestSamplePreparation(unittest.TestCase):

    def setUp(self):
        self.samples = load_samples_arff("test/iris.arff")

    def test_loading_arff(self):
        expected_meta = [NumericAttribute() for _ in xrange(4)]
        expected_cls_meta = NominalAttribute(
                    ["Iris-setosa", "Iris-versicolor", "Iris-virginica"])

        sample = self.samples[0]
        self.assertEqual(sample.meta, expected_meta)
        self.assertEqual(sample.cls_meta, expected_cls_meta)

    def test_spliting_samples(self):
        for _ in xrange(100):
            split_ratio = random.random()
            train, test = split_data(self.samples, split_ratio)
            self.assertEqual(math.ceil(len(self.samples) * split_ratio), len(train))
            self.assertEqual(len(self.samples), len(train) + len(test))

    def test_split_data_cv(self):
        N = 100
        for _ in xrange(100):
            samples = range(N)
            folds = random.randint(2, N / 3)
            sets = split_data_cv(samples, folds)
            for train, test in sets:
                for ts in test:
                    self.assertTrue(ts not in train)
                self.assertTrue(N / folds <= len(test) <= N / folds + 1)
                self.assertEqual(N, len(test) + len(train))
