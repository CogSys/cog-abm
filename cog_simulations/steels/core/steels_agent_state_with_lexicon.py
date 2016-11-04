from steels_agent_state import SteelsAgentState
from cog_simulations.cog_abm.extras.lexicon import Lexicon


class SteelsAgentStateWithLexicon(SteelsAgentState):

    def __init__(self, classifier, initial_lexicon=None):
        super(SteelsAgentStateWithLexicon, self).__init__(classifier)
        self.lexicon = initial_lexicon or Lexicon()

    def category_for(self, word):
        return self.lexicon.category_for(word)

    def word_for(self, category):
        return self.lexicon.word_for(category)
