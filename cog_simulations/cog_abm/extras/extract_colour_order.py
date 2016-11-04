'''
Module with functions for words storage.

Created on Dec 29, 2012

@author: mlukasik
'''
def extract_colour_order(stimuli, clab_name):
    '''
    Extract colour order from clab_fname and return stimuli in that order (exclude repetitions).
    '''
    chip_map = extract_chip_map(clab_name)
    return get_environment_in_order(stimuli, chip_map)
    
def get_environment_in_order(stimuli, chip_map):
    '''Return sorted list of stimuli from environment in order specified by 
    chip_map.
    '''
    visited = set()
    colour_order_keyed = []
    #traverse all stimuli and add them to the list, excluding repetitions
    for stimulus in stimuli:
        (L, a, b) = tuple(stimulus.get_values())
        if (L, a, b) not in visited:
            visited.add((L, a, b))
            float_values = (float(L), float(a), float(b))
            #if float_values not in chip_map:
            #    print "[get_environment_in_order]: ERROR!" + \
            #    "stimulus not in chip_map!"
            #    import sys
            #    sys.exit(1)
            colour_name = chip_map[float_values]
            colour_order_keyed.append((stimulus, colour_name))
    
    #sort by colour_name
    colour_order_keyed.sort(key = lambda x: x[1])
    #return only necessary part
    return [x[0] for x in colour_order_keyed]


def extract_chip_map(fname):
    """
    Read a chipmap from fname, extract information about which ordinal number
    is given to each of the Lab coordinates.
    """
    chip_map = {}
    with open(fname) as f:
        #each line is read from a c-lab file
        for line in f:
            line_list = line.split()
            #if it is already in a chip_map then there is some repetition!
            float_values = (float(line_list[6]), float(line_list[7]),
                            float(line_list[8]))
            #if float_values in chip_map:
            #    print "[extract_colour_order] ERROR!"+str(float_values)+ \
            #    "in chip_map !!!"
            #    import sys
            #    sys.exit(1)
            chip_map[float_values] = line_list[0]
    return chip_map