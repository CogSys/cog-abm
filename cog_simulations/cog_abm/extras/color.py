"""
Module providing definition of the Color class, implementing Perception's and
the Stimulus' interfaces.
"""
import os

from cog_simulations.cog_abm.ML.core import Sample, euclidean_distance


class Color(Sample):
    """
    Color represented in CIE L*a*b* space
    """

    def __init__(self,  l, a, b):
        """
        Initialize Color

        http://en.wikipedia.org/wiki/Lab_color_space
        section: Range_of_L.2Aa.2Ab.2A_coordinates

        @param l: lightness - should be in [0,100]
        @param a: can be negative
        @param b: can be negative
        """
        super(Color, self).__init__([l, a, b], dist_fun=euclidean_distance)
        self.L = l
        self.a = a
        self.b = b


def get_WCS_colors():
    from cog_simulations.parser import Parser
    return Parser().parse_environment(
        os.path.join(os.path.dirname(__file__), "../../../data/wcs_input_data/330WCS.xml")).stimuli


def get_1269Munsell_chips():
    from cog_simulations.parser import Parser
    return Parser().parse_environment("1269_munsell_chips.json", {}).stimuli
