from cog_classification.core.environment import Environment

from sklearn import datasets


class TestEnvironment:
    """
    Functions tested in TestEnvironment:
    - get_random_sample
    - get_random_sample_index
    - get_sample
    - get_samples

    Functions not tested:
    - __init__
    - standard_distance
    - get_all
    - get_all_classes
    - get_all_samples
    - get_class
    - set_distance
    """

    def __init__(self):
        irises = datasets.load_iris()
        self.env = Environment(irises.data, irises.target)

    def get_random(self):
        _, sample, _ = self.env.get_random_sample()
        return sample

    def get_index(self):
        index, _, _ = self.env.get_random_sample()
        return index

    def get_sample(self, index):
        return self.env.get_sample(index)

    def test_get_random_sample_multiple_sampling_gives_more_than_one_sample(self):
        sample = self.get_random()

        different = False

        for _ in range(1000):
            new_sample = self.get_random()
            if (new_sample == sample).all():
                different = True
                break

        assert different

    def test_get_random_sample_index_multiple_sampling_gives_more_than_one_sample(self):
        sample = self.get_index()

        different = False

        for _ in range(1000):
            new_sample = self.get_index()
            if new_sample == sample:
                different = True
                break

        assert different

    def test_get_sample_the_same_results_like_normal_indexes_x_100(self):
        irises = datasets.load_iris()

        for _ in range(100):
            index = self.get_index()
            assert (irises.data[index] == self.get_sample(index)).all()

    def test_get_samples_full_returned_array_identical_with_original(self):
        original = self.env.get_all_samples()
        copy = self.env.get_samples(range(len(original)))
        assert (original == copy).all()
