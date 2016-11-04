'''

Created on Dec 29, 2012

@author: mlukasik
'''
import sys
sys.path.append('../')
import unittest
from cog_abm.extras.extract_colour_order import get_environment_in_order

class TestGetEnvironmentInOrder(unittest.TestCase):

    def test_semi_reversed_order(self):
        
        class Colour(object):
            def __init__(self, val):
                self.val = val
            def get_values(self):
                return self.val
        
        stimuli = []
        ind = 1
        chip_map = {}
        for L in xrange(5):
            for a in xrange(5):
                stimuli.append( Colour((L, a, 0)) )
        
        expected_sequence = []
        for L in xrange(5):
            for a in reversed(range(5)):
                chip_map[(L, a, 0)] = ind
                ind += 1
                expected_sequence.append( (L, a, 0) )
        
        colour_sequence = get_environment_in_order(stimuli, chip_map)
        self.assertEqual(expected_sequence, \
                         map(lambda x: x.get_values(), colour_sequence))
        
if __name__ == '__main__':
    unittest.main()
