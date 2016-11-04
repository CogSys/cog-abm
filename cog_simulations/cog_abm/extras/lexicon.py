import random

#from tools import *
from itertools import groupby


class Syllable:

    allowed_syllables = ["a", "b", "c", "d", "e", "f", "g"]

    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

    def __str__(self):
        return str(self.content)

    @staticmethod
    def set_allowed_syllables(new_set):
        Syllable.allowed_syllables = new_set

    @staticmethod
    def get_random():
        return Syllable(random.choice(Syllable.allowed_syllables))


class Word(object):

    max_len = 5

    def __init__(self, syllables):
        self.syllables = syllables

    def __eq__(self, other):
        if other is None:
            return False
        #if isinstance(other, Word):
        return self.syllables == other.syllables
        #return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "".join([str(s) for s in self.syllables])

    def __repr__(self):
        return str(self)

    @staticmethod
    def set_max_len(n):
        Word.max_len = n

    @staticmethod
    def get_random():
        i = random.randint(1, Word.max_len)
        return Word([Syllable.get_random() for _ in xrange(i)])
        #return repr([Syllable.get_random() for i in range(i)])

    @staticmethod
    def get_random_not_in(words):
        w = Word.get_random()
        while w in words:
            w = Word.get_random()
        return w

    def __hash__(self):
        return hash(str(self))


class Lexicon(object):

    delta_inc = 0.1
    delta_inh = 0.1
    delta_dec = 0.1
    s = 0.5  # initial strength

    #L = C x F x [0.0, 1.0]
    def __init__(self, base=None):
        self.base = base or {}
        self.F = set()  # words

    def set_value(self, cord, weight):
        self.base[cord] = round(max(min(1., weight), 0.), 1)

    def add_element(self, category, word=None, weight=None):
        weight = weight or Lexicon.s
        word = word or Word.get_random_not_in(self.F)

        if word not in self.F:
            self.F.add(word)

        self.set_value((category, word), weight)
        return word

    def _find_best(self, choser):
        rval = (None, None)
        maxx = -float('inf')
        for k, v in self.base.iteritems():
            if choser(k) and v > maxx:
                maxx, rval = v, k

        return rval

    def word_for(self, category):
        return self._find_best(lambda k: k[0] == category)[1]

    def category_for(self, word):
        return self._find_best(lambda k: k[1] == word)[0]

    def decrease(self, category, word):
        w = self.base.pop((category, word)) - Lexicon.delta_dec
        self.set_value((category, word), w)

    def _decreaser(self, choser):
        for cat_word, v in self.base.items():
            if choser(cat_word):
                w = v - Lexicon.delta_inh
                self.set_value(cat_word, w)

    def do_inc_decrs(self, category, word, decrasers_filters):
        w = self.base.pop((category, word)) + self.delta_inc
        for fun in decrasers_filters:
            self._decreaser(fun)
        self.set_value((category, word), w)

    def inc_dec_categories(self, category, word):
        self.do_inc_decrs(category, word, [lambda k: k[1] == word])

    def inc_dec_words(self, category, word):
        self.do_inc_decrs(category, word, [lambda k: k[0] == category])

    def increase_pair_decrease_other(self, category, word):
        self.do_inc_decrs(category, word, [
            lambda k: k[1] == word,
            lambda k: k[0] == category]
            )

    def known_words(self):
        return set(self.base.values())

    def __str__(self):
        gb = groupby(self.base.iteritems(), key=lambda (k, v): k[1])
        return "Lexicon:" + "\t".join(
            ["(\"%s\":%s)" % (w, [(c, s) for (c, w), s in list(g)])
                for w, g in gb])
