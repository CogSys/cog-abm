from nose.tools import assert_equals, raises

from cog_classification.steels.lexicon import Lexicon


class TestLexicon:
    """
    Functions tested in TestLexicon:
    - __init__
    - add_new_category
    - add_word_to_category
    - find_category_for_word
    - remove_category
    - increase_weight
    - decrease_weight
    - weaken_other_associations_for_categories
    - decrease_weights_for_other_words
    - find_word_for_category

    Functions not tested:
    - get_words
    - get_words_size
    - get_categories_size
    """

    def __init__(self):
        self.lexicon = None

    def add_category(self, category, word=None, weight=None):
        return self.lexicon.add_new_category(category, word, weight)

    def add_word(self, category, word, weight=None):
        self.lexicon.add_word_to_category(word, category, weight)

    def categories_size(self, size):
        assert_equals(self.lexicon.get_categories_size(), size)

    def category_and_word(self, category, word):
        self.category_for_word(category, word)
        self.word_for_category(category, word)

    def category_for_word(self, category, word):
        assert_equals(self.lexicon.find_category_for_word(word), category)

    def word_for_category(self, category, word):
        assert_equals(self.lexicon.find_word_for_category(category), word)

    def words_size(self, size):
        assert_equals(self.lexicon.get_words_size(), size)

    def setup(self):
        self.lexicon = Lexicon()

    @raises(AssertionError)
    def test__init__forbidden_value_decrease_strength_bigger_than_max_strength(self):
        l = Lexicon(weight_decrease=1, max_weight=0)

    @raises(AssertionError)
    def test__init__forbidden_value_decrease_strength_lower_than_0(self):
        l = Lexicon(weight_decrease=-1)

    @raises(AssertionError)
    def test__init__forbidden_value_increase_strength_bigger_than_max_strength(self):
        l = Lexicon(weight_increase=1, max_weight=0)

    @raises(AssertionError)
    def test__init__forbidden_value_increase_strength_lower_than_0(self):
        l = Lexicon(weight_increase=-1)

    @raises(AssertionError)
    def test__init__forbidden_value_initial_strength_bigger_than_max_strength(self):
        l = Lexicon(max_weight=1, new_weight=2)

    @raises(AssertionError)
    def test__init__forbidden_value_initial_strength_lower_than_min_strength(self):
        l = Lexicon(min_weight=1, new_weight=0)

    @raises(AssertionError)
    def test__init__forbidden_value_lateral_inhibition_bigger_than_max_strength(self):
        l = Lexicon(lateral_inhibition=1, max_weight=0)

    @raises(AssertionError)
    def test__init__forbidden_value_lateral_inhibition_lower_than_0(self):
        l = Lexicon(lateral_inhibition=-1)

    @raises(AssertionError)
    def test__init__forbidden_value_max_lower_than_min(self):
        l = Lexicon(min_weight=1, max_weight=0)

    @raises(AssertionError)
    def test__init__forbidden_value_min_lower_than_0(self):
        l = Lexicon(min_weight=-1)

    def test_add_new_category_returns_good_values(self):
        assert_equals(self.add_category(1, 1), 1)
        assert_equals(self.add_category(2, 2), 2)
        assert_equals(self.add_category(3, 3), 3)
        assert_equals(self.add_category(2), None)

        word = self.add_category(4)
        self.category_and_word(4, word)

    def test_add_word_to_category_good_weights(self):
        self.add_category(1, 1, 0.1)
        self.category_and_word(1, 1)

        self.add_word(1, 2, 0.2)
        self.category_and_word(1, 2)

        self.add_word(1, 3, 0.3)
        self.category_and_word(1, 3)

    @raises(ValueError)
    def test_add_word_to_category_none_category_error(self):
        self.lexicon.add_word_to_category(1, None)

    def test_remove_category_adding_and_removing_to_empty(self):
        self.test_word_for_category_adding_new_words_and_categories()
        self.add_word(1, 3, 0.1)
        self.words_size(3)
        self.categories_size(2)

        self.lexicon.remove_category(1)
        self.words_size(2)
        self.categories_size(1)

        self.lexicon.remove_category(2)
        self.words_size(0)
        self.categories_size(0)

    def test_remove_category_re_adding_elements_after_remove(self):
        self.test_remove_category_adding_and_removing_to_empty()
        self.test_remove_category_adding_and_removing_to_empty()

    def test_strengthen_association_bigger(self):
        self.add_category(1, 1, 0.1)
        self.add_word(1, 2, 0.2)
        self.category_and_word(1, 2)
        self.category_for_word(1, 1)

        self.lexicon.increase_weight(1, 1)
        self.lexicon.increase_weight(1, 1)

        self.category_and_word(1, 1)
        self.category_for_word(1, 2)

    def test_weaken_association_lower(self):
        self.add_category(1, 1)
        self.add_category(2, 1)
        self.add_word(1, 2)

        self.lexicon.decrease_weight(2, 1)
        self.lexicon.decrease_weight(1, 2)

        self.category_and_word(1, 1)

    def test_weaken_other_associations_for_categories_lower(self):
        self.add_category(1, 1, 0.1)
        self.add_category(2, 1, 0.2)
        self.add_category(3, 1, 0.0)
        self.add_category(4, 1, 0.3)
        self.category_and_word(4, 1)

        self.lexicon.decrease_weights_for_other_categories(1, 1)
        self.lexicon.decrease_weights_for_other_categories(1, 1)
        self.lexicon.decrease_weights_for_other_categories(1, 1)

        self.category_and_word(1, 1)
        self.word_for_category(2, 1)
        self.word_for_category(3, 1)
        self.word_for_category(4, 1)

    def test_weaken_other_associations_for_words_lower(self):
        self.add_category(1, 1, 0.1)
        self.add_word(1, 2, 0.2)
        self.add_word(1, 3, 0)
        self.add_word(1, 4, 0.3)
        self.category_and_word(1, 4)

        self.lexicon.decrease_weights_for_other_words(1, 1)
        self.lexicon.decrease_weights_for_other_words(1, 1)
        self.lexicon.decrease_weights_for_other_words(1, 1)

        self.category_and_word(1, 1)
        self.category_for_word(1, 2)
        self.category_for_word(1, 3)
        self.category_for_word(1, 4)

    def test_word_for_category_adding_new_words_and_categories(self):
        """ And test_category_for_word. """
        self.add_category(1, 1, 0.1)
        self.category_and_word(1, 1)

        self.add_category(2, 1, 0.2)
        self.category_and_word(2, 1)
        self.word_for_category(1, 1)

        self.add_word(1, 2, 0.2)
        self.category_and_word(2, 1)
        self.category_and_word(1, 2)

        self.add_word(2, 2, 0.1)
        self.category_and_word(2, 1)
        self.category_and_word(1, 2)
