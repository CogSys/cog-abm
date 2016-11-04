'''

Created on Dec 30, 2012

@author: mlukasik

Compute statistics on words - result of cog_abm simulation. 

Simple statistics for the set of colours seperated into 2 subsets, based on one coordinate.
Point of division is median.
'''
from utils import get_mode_word_stats, string2prefix_num, is_number

#statistics to be calculated; their names must correspond to methods in numpy package
STATISTICS_MEASURES = ['average', 'median', 'std']

def get_numpy_statistics(data, statistics_measures):
    '''
    For a given list return a statistics specified by STATISTICS_MEASURES.
    '''
    import numpy
    statistics = {}
    for stat in statistics_measures:
        statistics[stat] = getattr(numpy, stat)(data)
    return statistics
        
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Parameter 1: a file with words in c-lab format."
        exit(1)
    clab_fname = sys.argv[1]#plik z c-lab
    if len(sys.argv) < 3:
        print "Parameter 2: an integer corresponding to a coordinate by which colours are separated."
        exit(1)
    coordinate = int(sys.argv[2])#podzial wzgledem ktorej wspolrzednej
    if len(sys.argv) < 4:
        print "Parameter 3: catalogue, where results of a simulation are stored."
        exit(1)
    cat = sys.argv[3]#katalog z wynikami

    import os
    cats = map(lambda x: cat+"//"+x, os.listdir(cat))
    #assume that in each catalogue there are files named the same, which correspond to one another
    files = os.listdir(cats[0])

    #for plotting purposes:
    medians = []
    means = []
    xvals = []
    
    #how many simulations chose bigger, how many chose smaller
    mode_bigger = {}
    #list statistics for each file, gathering info from all catalogues:
    for fname in sorted(files, key=lambda x: string2prefix_num(x)):
        mode_bigger[fname] = [0, 0]
        #all results_of_simulation for left and all results_of_simulation for right
        all_results_modes = []
        all_results_words = []
        for cat in cats:
            bigger_mode, smaller_mode, avg_wordnum1, avg_wordnum2 = \
            get_mode_word_stats(cat+"/"+fname, clab_fname, coordinate)
            
            if bigger_mode > smaller_mode:
                mode_bigger[fname][0] += 1
            elif bigger_mode < smaller_mode:
                mode_bigger[fname][1] += 1
            
            all_results_modes += [(bigger_mode, smaller_mode)] 
            all_results_words += [(avg_wordnum1, avg_wordnum2)]
        
        #=====calculate statistics for current fname=====#
        statistics = [{}, {}]
        for ind in [0, 1]:#index of half
            sub_stats = {}
            sub_stats = get_numpy_statistics( map(lambda x: x[ind], \
                                                        all_results_modes), \
                                             STATISTICS_MEASURES )
            for key in sub_stats.iterkeys():
                statistics[ind]['mode_'+key] = sub_stats[key]
            
            sub_stats = get_numpy_statistics( map(lambda x: x[ind], \
                                                        all_results_words), \
                                             STATISTICS_MEASURES )
            for key in sub_stats.iterkeys():
                statistics[ind]['wordnum_'+key] = sub_stats[key]
            
        
        #=====print results for current fname=====#
        print str(string2prefix_num(fname))+":"
        
        def printable_elem(s):
            #check if integer
            try:
                int(s)
                return str(s)
            except:
                #check if float:
                if is_number(s):
                    return "%.4f" % s
                else:
                    return s
            
        #print header
        res_line = ["Bigger_wins", "Smaller_wins", "|"] + \
            map(lambda x: "mode_"+x, STATISTICS_MEASURES) + \
            ["|"] + \
            map(lambda x: "word_number_"+x, STATISTICS_MEASURES)
        print "\t".join([printable_elem(res) for res in res_line])
        
        for ind in [0, 1]:#index of half
            res_line = []
            res_line.append( mode_bigger[fname][0] )
            res_line.append( mode_bigger[fname][1] )
            res_line.append( "|" )
            
            for key in STATISTICS_MEASURES:
                res_line.append( statistics[ind]['mode_'+key] )
            res_line.append( "|" )
                
            for key in STATISTICS_MEASURES:
                res_line.append( statistics[ind]['wordnum_'+key] )
            
            print "\t".join([printable_elem(res) for res in res_line])
        
        xvals.append(string2prefix_num(fname))
        medians.append((statistics[0]['mode_'+STATISTICS_MEASURES[1]], statistics[1]['mode_'+STATISTICS_MEASURES[1]]))
        means.append((statistics[0]['mode_'+STATISTICS_MEASURES[0]], statistics[1]['mode_'+STATISTICS_MEASURES[0]]))
    import numpy as np
    import matplotlib.pyplot as plt

    #plt.plot(xvals, map(lambda x: x[0], medians), 'r--', xvals, map(lambda x: x[1], medians), 'b')
    #plt.savefig("median.png")
    #plt.close()
	
    #plt.plot(xvals, map(lambda x: x[0], means), 'r--', xvals, map(lambda x: x[1], means), 'b')
    #plt.savefig("avg.png")

    print "srednia mediana:", sum([x[0] - x[1] for x in medians])*1.0/len(medians)
    print "srednia sredniej:", sum([x[0] - x[1] for x in means])*1.0/len(medians)
