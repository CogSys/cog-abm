'''
Module with functions for words storage.

Created on Dec 29, 2012

@author: mlukasik 
'''
def store_words(agents, colour_order, out_file):
    """Stores words used by agents to a file.
    
    agents - list of agents
    colour_order - list of colours as they are going to be passed to agents for namings
    out_file - output file name to store results
    
    """
    agents_words_string = get_agents_words(agents, colour_order)
    agents_words_numerical = convert2numerical(agents_words_string)
    save_words_to_file(agents_words_numerical, out_file)
    
def get_agents_words(agents, colour_order):
    """
    Extract agents' words assigned to each of the stimuli from colour_order.
    
    """
    #a dictionary mapping agent to a list of namings for consecutive colours:
    agentsdict = {}
    for colour in colour_order:#stimuli:
        #add this colour to each agent:
        for ind, agent in enumerate(agents):
            #print agent.sense_and_classify(colour), 
            word = agent.state.word_for(agent.sense_and_classify(colour))
            agentsdict[ind] = agentsdict.get(ind, []) + [word]
            
    return agentsdict
    
def convert2numerical(agents_words):
    """ 
    Convert agents_words into a numerical format, switching from string representation of words.
    Each colour gets a positive integer assigned. An exceptions is -1, which is reserved for 'None'. 
    
    >>> convert2numerical({0: ["a", "b", "c", "b", 'None'], 1: ["a", "c", "e", "b", "f"]})
    {0: [1, 2, 3, 2, -1], 1: [1, 3, 4, 2, 5]}
    """
    numerical_words = {}
    occured_words = {}
    occured_words['None'] = -1
    occured_words[None] = -1
    next_val = 1
    
    for agent_id in agents_words.iterkeys():
        for colour in agents_words[agent_id]:
            if colour not in occured_words:
                occured_words[colour] = next_val
                next_val += 1
            numerical_words[agent_id] = \
             numerical_words.get(agent_id, []) + [occured_words[colour]]
    return numerical_words
    
                
def save_words_to_file(agents_words, fname):
    """ 
    Save agents_words to a file named fname.
    
    """
    with open(fname, 'w') as f:
        for agent_id in agents_words.iterkeys():
            f.write(str(agent_id)+" ")
            for colour in agents_words[agent_id]:
                #print key#print "[save_words_to_file] key", key
                f.write(str(colour)+" ")
            f.write("\n")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
