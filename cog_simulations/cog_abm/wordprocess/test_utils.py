'''
Created on Jan 2, 2013

@author: mlukasik
'''
import unittest
from utils import *


class TestGetWordCount(unittest.TestCase):

    def test_case1(self):
        words_per_agent = {0: ["a", "b", "c", "b", 'None'],
                           1: ["a", "c", "e", "b", "f"],
                           2: ["b", "c", "r", 'None', 'None']}
        
        expected_result = {0: {"a": 2, "b": 1}, 1: {"b": 1, "c": 2}, 
                           2: {"c": 1, "e": 1, "r": 1},
                           3: {"b": 2, 'None': 1},
                           4: {'None': 2, "f": 1}}
        
        self.assertEqual(get_word_count(words_per_agent, nullify=False), expected_result)
        
class TestGetModaFractionListPerSet(unittest.TestCase):

    def test_case1(self):
        
        word_count = {0: {"a": 2, "b": 1}, 1: {"b": 1, "c": 2}, 
                           2: {"c": 1, "e": 1, "r": 1},
                           3: {"b": 2, 'None': 1},
                           4: {'None': 2, "f": 1}}
        
        set1 = {0, 1, 2}
        set2 = {3, 4}
        expected_result1 = [2.0/3, 2.0/3, 1.0/3]
        expected_result2 = [2.0/3, 2.0/3]
        
        result = get_moda_fraction_list_per_set(word_count, set1, set2)
        
        self.assertEqual(result, (expected_result1, expected_result2))

class TestAvgNumOfWordsPerAgentForSets(unittest.TestCase):

    def test_case1(self):
        
        words_per_agent = {0: ["a", "b", "c", "b", 'None'],
                           1: ["a", "c", "e", "b", "f"],
                           2: ["b", "c", "r", 'None', 'None']}
        
        set1 = {0, 1, 2}
        set2 = {3, 4}
        expected_result1 = (2 + 2 + 3)*1.0/3
        expected_result2 = (2 + 2)*1.0/2
        
        result = avg_num_of_words_per_agent_for_sets(words_per_agent, set1, set2)
        
        self.assertEqual(result, (expected_result1, expected_result2))

if __name__ == '__main__':
    unittest.main()
