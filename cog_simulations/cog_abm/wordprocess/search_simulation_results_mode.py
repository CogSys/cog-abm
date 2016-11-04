'''

Created on June 7, 2013

@author: mlukasik
'''

from os import listdir
from os.path import isfile, join

from gather_mode_analysis_simple import gather_repeated_simulation_statistics

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
    outer_cat = sys.argv[3]#katalog z katalogami z wynikami
    if len(sys.argv) < 5:
        print "Parameter 4: what statistic to look for extremum of (example: mode_average)"
        exit(1)
    stat_name = sys.argv[4]#katalog z katalogami z wynikami
    if len(sys.argv) < 6:
        print "Parameter 5: what std statistic to check (example: mode_std)"
        exit(1)
    std_name = sys.argv[5]#katalog z katalogami z wynikami
    
    
    
    catalogues_with_subres = [ f for f in listdir(outer_cat)]
    
    minimum_name = "NOTHING"
    minimum_diff = 10000
    minimum_std = -1
    
    maximum_name = "NOTHING"
    maximum_diff = -10000
    maximum_std = -1
    
    for inner_cat in catalogues_with_subres:
        print "Checking:", inner_cat
        try:#try, because let's give the opportunity to call this script, when the simulations have not finished (so a catalogue may be empty
            statistics, mode_bigger, files = gather_repeated_simulation_statistics(clab_fname, coordinate, outer_cat+"/"+inner_cat)
            
            val = statistics[files[-1]][0][stat_name] - statistics[files[-1]][1][stat_name]
            
            if val > maximum_diff:
                maximum_name = inner_cat
                maximum_diff = val
                maximum_std = (statistics[files[-1]][0][std_name], statistics[files[-1]][1][std_name])
            
            if val < minimum_diff:
                minimum_name = inner_cat
                minimum_diff = val
                minimum_std = (statistics[files[-1]][0][std_name], statistics[files[-1]][1][std_name])
        except:
            break

    print "====================================="
    print "Maximum difference between 0 and 1:"
    print "maximum_name:", maximum_name
    print "maximum_diff:", maximum_diff
    print "maximum_std:", maximum_std
    
    print "====================================="
    print "Minimum difference between 0 and 1:"
    print "minimum_name:", minimum_name
    print "minimum_diff:", minimum_diff
    print "minimum_std:", minimum_std
    
