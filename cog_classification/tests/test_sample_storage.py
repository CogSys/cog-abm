from itertools import izip_longest

from nose.tools import assert_equals, raises

from cog_classification.steels.sample_storage import SampleStorage
from dummy_classes.dummy_environment import DummyEnvironment


class TestSampleStorage:
    """
    Functions tested in TestSampleStorage:
    - add_sample
    - create_new_category
    - decrease_weights_in_category
    - export
    - increase_weights_in_category
    - remove_category
    - remove_sample_from_category
    - remove_samples_with_low_weights_from_category

    Functions not tested:
    - __init__
    - decrease_weights
    - empty
    - remove_samples_with_low_weights
    - sample_in_category
    - get_category_samples
    - get_category_samples_size
    - get_categories
    - get_categories_size
    - get_class
    - set_distance
    - set_weight
    """

    def __init__(self):
        self.storage = None

        self.env = DummyEnvironment()

    def assert_size(self, number):
        """ number == number of categories in sample storage """
        assert_equals(self.storage.get_categories_size(), number)

    def assert_samples_size(self, number, category):
        """ number == number of samples in category in sample storage """
        assert_equals(self.storage.get_category_samples_size(category), number)

    def add(self, sample, environment=None, category=None, sample_weight=None):
        environment = environment or self.env

        self.storage.add_sample(sample, environment, category, sample_weight)

    def setup(self):
        self.storage = SampleStorage()

    def test_1(self):
        """ Adding sample without category. """
        self.assert_size(0)

        self.add(1)

        self.assert_size(1)

    def test_2(self):
        """ Adding sample with not existing category. """
        self.assert_size(0)

        self.add(1, category=1)

        self.assert_size(1)
        self.assert_samples_size(1, 1)

    def test_3(self):
        """ Adding sample with other class than category. """
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        self.add(11, category=1)

        self.assert_size(2)
        self.assert_samples_size(1, 1)

    def test_4(self):
        """ Adding already existing sample to the same category. """
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        self.add(1, category=1)

        self.assert_size(1)
        self.assert_samples_size(1, 1)

    def test_5(self):
        """ Adding already existing sample to other category. """
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        self.add(1, category=2)

        self.assert_size(1)
        self.assert_samples_size(1, 1)

    def test_6(self):
        """ Adding already existing sample with no category. """
        self.add(1)
        self.assert_size(1)

        self.add(1)

        self.assert_size(1)

    def test_7(self):
        """ Sophisticated adding sample test. """
        self.assert_size(0)

        # Adding new element to non existing class.
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        # Adding old element to existing class.
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        # Adding new element to existing class.
        self.add(2, category=1)
        self.assert_size(1)
        self.assert_samples_size(2, 1)

        # Adding new element to non existing class.
        self.add(3, category=2)
        self.assert_size(2)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)

        # Adding existing element to existing class.
        self.add(3, category=1)
        self.assert_size(2)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)

        # Adding new element to non existing class.
        self.add(4, category=3)
        self.assert_size(3)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element to existing class (different true categories).
        self.add(15, category=3)
        self.assert_size(4)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element to existing class (different true categories).
        self.add(25, category=1)
        self.assert_size(5)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element without class.
        self.add(54)
        self.assert_size(6)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        env = DummyEnvironment()
        # Adding element with the same index but with different environment.
        self.add(1, env, 1)
        self.assert_size(6)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element with different environment and true class.
        self.add(63, env, 3)
        self.assert_size(7)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

    def test_8(self):
        """ Adding new samples with categories don't create conflicts with sample storage categories generator. """
        self.add(1, category="Category number: 0")
        self.add(2, category="Category number: 1")
        self.add(3, category="Category number: 2")
        self.add(4, category="Category number: 4")

        self.assert_size(4)
        self.add(5)
        self.assert_size(5)
        self.add(6)
        self.assert_size(6)

        categories = self.storage.get_categories()

        for name in ["Category number: 3", "Category number: 5"]:
            find_class = False

            for c in categories:
                if name == c:
                    find_class = True
                    break

            assert find_class

    def test_9(self):
        """ Decreasing weights in category lowers weights. """
        self.add(1, self.env, 1, 1)
        self.add(21, self.env, 1, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 1)

        self.storage.decrease_weights_in_category(1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert weight < 1

    def test_10(self):
        """ Decreasing weights in category never decrease weights under 0. """
        self.add(1, self.env, 1, 0.01)
        self.add(21, self.env, 1, 0.01)

        for _ in range(1000):
            self.storage.decrease_weights_in_category(1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert weight >= 0

    def test_11(self):
        """ Sample storage export their samples correctly. """
        samples1 = []
        classes1 = []

        for i in range(10):
            for j in range(10):
                self.add(i * 10 + j, category=i)
                samples1.append(i * 10 + j)
                classes1.append(i)

        samples2, classes2 = self.storage.export()

        # Checking whether for every sample and class in samples1 and classes1
        # exist exactly same pair in samples2 and classes2.
        for sample1, class1 in izip_longest(samples1, classes1):
            pair_find = False
            for sample2, class2 in izip_longest(samples2, classes2):
                if (sample1 == sample2).all() and class1 == class2:
                    pair_find = True
                    break

            if not pair_find:
                print(sample1, class1)
                print(samples2, classes2)
            assert pair_find

        # Checking whether for every sample and class in samples2 and classes2
        # exist exactly same pair in samples1 and classes1.
        for sample2, class2 in izip_longest(samples2, classes2):
            pair_find = False
            for sample1, class1 in izip_longest(samples1, classes1):
                if (sample1 == sample2).all() and class1 == class2:
                    pair_find = True
                    break

            if not pair_find:
                print(sample2, class2)
                print(samples1, classes1)
            assert pair_find

    def test_12(self):
        """ Increasing weights in category increases weights. """
        self.add(1, self.env, 1, 0)
        self.add(2, self.env, 1, 0)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 0)

        self.storage.increase_weights_in_category(1, self.env, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert weight > 0

    def test_13(self):
        """ Increasing weights in category doesn't increase weights over max weight (1). """
        self.add(1, self.env, 1, 1)
        self.add(2, self.env, 1, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 1)

        self.storage.increase_weights_in_category(1, self.env, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 1)

    @raises(KeyError)
    def test_14(self):
        """ Removing category from empty storage fails. """
        self.storage.remove_category(1)

    @raises(KeyError)
    def test_15(self):
        """ Removing category from storage without this category fails. """
        self.add(1, category=1)
        self.storage.remove_category(2)

    def test_16(self):
        """ Removing all categories from full storage leaves it empty. """
        self.test_7()
        categories = self.storage.get_categories()
        categories_size = self.storage.get_categories_size()

        for removed_category in categories:
            self.assert_size(categories_size)
            self.storage.remove_category(removed_category)
            categories_size -= 1

        self.assert_size(0)

    def test_17(self):
        """ Adding samples to removed category restore this category without problems. """
        self.assert_size(0)
        self.add(1, category=1)
        self.assert_size(1)
        self.storage.remove_category(1)
        self.assert_size(0)
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

    @raises(KeyError)
    def test_18(self):
        """ Removing sample from empty storage fails. """
        self.storage.remove_sample_from_category(self.env, 1, sample_index=1)

    @raises(TypeError)
    def test_19(self):
        """ Removing sample from category without sample fails. """
        self.add(1, self.env, 1)
        self.add(11, category=2)
        self.storage.remove_sample_from_category(self.env, 1, sample=11)

    @raises(KeyError)
    def test_20(self):
        """ Removing sample from empty category fails. """
        self.add(1, category=1)
        self.storage.remove_sample_from_category(self.env, 2, sample_index=1)

    def test_21(self):
        """ Removing last sample from category removes category. """
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        self.storage.remove_sample_from_category(self.env, 1, sample_index=1)
        self.assert_size(0)

    @raises(KeyError)
    def test_22(self):
        """ Removing weak samples from empty storage fails. """
        self.storage.remove_samples_with_low_weights_from_category(1)

    def test_23(self):
        """ Removing weak samples from category can remove category. """
        self.add(1, self.env, 1, 0)
        self.add(2, self.env, 1, 0)
        self.add(3, self.env, 1, 0)

        self.assert_size(1)
        self.storage.remove_samples_with_low_weights_from_category(1)
        self.assert_size(0)

    def test_24(self):
        """ Removing weak samples from category doesn't affect other categories. """
        self.add(1, self.env, 1, 0)
        self.add(2, self.env, 1, 0)
        self.add(3, self.env, 1, 0)

        self.add(12, self.env, 2, 0)
        self.add(23, self.env, 3, 0)
        self.add(34, self.env, 4, 0)

        self.assert_size(4)
        self.storage.remove_samples_with_low_weights_from_category(1)
        self.assert_size(3)
