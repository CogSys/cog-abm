import random


class Lexicon:
    """
    Storage of associations between categories and words.

    :param dictionary dictionary: representation of associations between words and categories. \
        Words are keys and dictionaries - {category: weight} are values.
    :param dictionary categories: represents lists of words that have association with given category. \
        Categories are keys and lists of words are values.
    :param float min_weight: minimal weight of association. Values from 0 to infinity.
    :param float max_weight: maximal weight of association. Values from min weight to infinity.
    :param float new_weight: the weight of new association added to lexicon. Value form min_weight to max weight.
    :param float weight_increase: how much weight of association will be increased. Value from 0 to max weight.
    :param float weight_decrease: how much weights of associations will be decreased when we inhibit associations \
        between category and words. value from 0 to max weight.
    :param float lateral_inhibition: how much weights of associations will be decreased when we inhibit associations \
        between word and categories. value from 0 to max weight.
    :param long word_range: the size of pool of words in word generator. \
        The generated words are longs from range(word_range). Value from 0 to infinity.

    Every word can be associated with multiple categories and vice versa.

    Association is described by weight.
    """

    def __init__(self, dictionary=None, categories=None, min_weight=0, max_weight=1, new_weight=0.5,
                 weight_increase=0.1, weight_decrease=0.1, lateral_inhibition=0.1, word_range=100000):

        # Dictionary: {word: {category: weight}}
        self.dictionary = dictionary or {}
        # Categories: {category: [words]}
        self.categories = categories or {}

        assert min_weight >= 0
        self.min_weight = min_weight

        assert max_weight >= min_weight
        self.max_weight = max_weight

        assert new_weight >= min_weight
        assert new_weight <= max_weight
        self.new_weight = new_weight

        assert weight_increase >= 0
        assert weight_increase <= max_weight
        self.weight_increase = weight_increase

        assert lateral_inhibition >= 0
        assert lateral_inhibition <= max_weight
        self.lateral_inhibition = lateral_inhibition

        assert weight_decrease >= 0
        assert weight_decrease <= max_weight
        self.weight_decrease = weight_decrease

        assert word_range > 0
        self.word_range = word_range

    def add_new_category(self, category, word=None, weight=None):
        """
        Adds new category to lexicon.

        :param hashable category: the category that is added.
        :param hashable word: the word that should be associated with category.
        :param float weight: the weight of association between word (given or created) and category. \
            Value from min weight to max weight.

        :return: the word that is associated with new category or None if category already in lexicon.
        :rtype: hashable or None

        If word isn't specified lexicon creates new unique word for category.
        If weight isn't specified lexicon uses new weight.
        If category already in lexicon - returns None.
        """
        if category in self.categories:
            return None
        else:
            if weight is None:
                weight = self.new_weight
            else:
                assert weight <= self.max_weight
                assert weight >= self.min_weight

            if word is None:
                word = self.generate_word()

            if word not in self.dictionary:
                self.dictionary[word] = {category: weight}
            else:
                self.dictionary[word][category] = weight

            self.categories[category] = [word]

            return word

    def add_word_to_category(self, word, category, weight=None):
        """
        Add new word to category.

        :param hashable word: the word that is added.
        :param hashable category: the category that should be associated with the word.
        :param float weight: the weight of association between word and category. Value from min weight to max weight.

        :raise: **ValueError** - if category or word is None.

        If weight isn't specified lexicon uses new weight.
        If category doesn't exist, lexicon adds new category.
        If word already in category, nothing happens.
        """

        if word is not None:
            # If category has already existed.
            if category in self.categories:
                # If word hasn't been add already to category.
                if word not in self.categories[category]:
                    # Determine weight of association.
                    if weight is None:
                        weight = self.new_weight
                    else:
                        assert weight <= self.max_weight
                        assert weight >= self.min_weight

                    # Adding word to category.
                    self.categories[category].append(word)

                    # Updating or adding word to lexicon's dictionary.
                    if word in self.dictionary:
                        self.dictionary[word][category] = weight
                    else:
                        self.dictionary[word] = {category: weight}

            # Category doesn't exist so we add it with a word.
            # Word is updated or added to lexicon's dictionary by add_new_category method.
            elif category is not None:
                self.add_new_category(category, word, weight)
            # If category is None.
            else:
                raise ValueError
        # If word is None.
        else:
            raise ValueError

    def decrease_weight(self, word, category):
        """
        Decrease association's weight between word and category.

        :param hashable word: the word.
        :param hashable category: the category.

        :raise: **KeyError** - if word isn't in lexicon or no association between word and category.
        """
        self.dictionary[word][category] -= self.weight_decrease

    def decrease_weights_for_other_categories(self, word, category):
        """
        Decrease association's weights between categories other than specified and word.

        :param hashable word: the word.
        :param hashable category: the only category which association's weight won't be decreased.

        :raise: **KeyError** - if word isn't in lexicon.
        """
        for other_category in self.dictionary[word]:
            if not other_category == category:
                self.dictionary[word][other_category] -= self.lateral_inhibition

    def decrease_weights_for_other_words(self, word, category):
        """
        Decrease association's weights between words other than specified and category.

        :param hashable word: the only word, which association's weight won't be decreased.
        :param hashable category: the category.

        :raise: **KeyError** - if word or category isn't in lexicon or no association between word and category.
        """
        for other_word in self.categories[category]:
            if not other_word == word:
                new_weight = max(self.min_weight, self.dictionary[word][category] - self.lateral_inhibition)
                self.dictionary[other_word][category] = new_weight

    def find_category_for_word(self, word):
        """
        Finds category with the strongest association with word.

        :param hashable word: the word for which the best category is searched.

        :return: the category with the strongest association with word or None if word isn't in lexicon.
        :rtype: hashable or None
        """
        best_category = None
        best_weight = -float('inf')

        if word in self.dictionary:
            for category in self.dictionary[word]:
                element_weight = self.dictionary[word][category]
                if element_weight > best_weight:
                    best_category = category
                    best_weight = element_weight

        return best_category

    def find_word_for_category(self, category):
        """
        Finds word with the strongest association with category.

        :param hashable category: the category for which the best word is searched.

        :return: the word with the strongest association with category.
        :rtype: hashable

        If no such category in lexicon then category is added in lexicon and returned is new generated word.
        """
        best_word = None
        best_weight = -float('inf')

        if category in self.categories:
            for word in self.categories[category]:
                element_weight = self.dictionary[word][category]
                if element_weight > best_weight:
                    best_word = word
                    best_weight = element_weight
        else:
            best_word = self.add_new_category(category)

        return best_word

    def generate_word(self):
        """
        :return: new word that isn't in lexicon.
        :rtype: long
        """
        new_word = random.randrange(self.word_range)
        while new_word in self.dictionary:
            new_word = random.randrange(self.word_range)
        return new_word

    def get_categories(self):
        """
        :return: all categories of lexicon.
        :rtype: list of hashable
        """
        return self.categories.keys()

    def get_categories_size(self):
        """
        :return: number of categories in the lexicon.
        :rtype: long
        """
        return len(self.categories)

    def get_words(self):
        """
        :return: all words of lexicon.
        :rtype: list of hashable
        """
        return self.dictionary

    def get_words_size(self):
        """
        :return: number of words in the lexicon.
        :rtype: long
        """
        return len(self.dictionary)

    def increase_weight(self, word, category):
        """
        Increase association's weight between word and category.

        :param hashable word: the word.
        :param hashable category: the category.

        If word and category don't have any association yet, then new association between them is added.
        """
        if category in self.dictionary[word]:
            new_weight = min(self.max_weight, self.dictionary[word][category] + self.weight_increase)
            self.dictionary[word][category] = new_weight
        else:
            self.add_word_to_category(category, word)

    def remove_category(self, category):
        """
        Removes given category.

        :param hashable category: the category to remove.

        If it was the last category for word it removes this word, too.
        """
        if category in self.categories:
            words_to_remove = []

            for word in self.categories[category]:
                self.dictionary[word].pop(category)
                if len(self.dictionary[word]) == 0:
                    words_to_remove.append(word)

            self.categories.pop(category)

            for word in words_to_remove:
                self.dictionary.pop(word)
