'''

Created on Dec 30, 2012

@author: mlukasik

Plot statistics on words along the iteration numbers. 

Simple statistics for the set of colours seperated into 2 subsets, based on one coordinate.
Point of division is median.
'''
from utils import get_mode_word_stats, string2prefix_num, is_number
from gather_mode_analysis_simple import STATISTICS_MEASURES, get_numpy_statistics, gather_repeated_simulation_statistics, printable_elem
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
    if len(sys.argv) < 5:
        print "Parameter 4: measured statistic to plot, for example 'median'."
        exit(1)
    measured_statistic = sys.argv[4]

    statistics, mode_bigger, files = gather_repeated_simulation_statistics(clab_fname, coordinate, cat)

    x = []
    y1 = []
    y2 = []
    ydiff = []
    ydiffstd = []
    for fname in sorted(files, key=lambda x: string2prefix_num(x)):
        #=====print results for current fname=====#
        x.append(string2prefix_num(fname))
        for ind, y in enumerate([y1, y2]):
            y.append(statistics[fname][ind]['mode_'+measured_statistic])
        ydiffstd.append(statistics[fname][0]['mode_std']+statistics[fname][1]['mode_std'])
    
    for i in xrange(len(x)):
        ydiff.append(y1[i]-y2[i])
    
    #===================================================================
    #PLOT
    #===================================================================
    
    import numpy as np
    import matplotlib.pyplot as plt

    variance = np.var(ydiff)
    plt.ylim(ymin = -0.1, ymax = 0.1)
    plt.errorbar(x, ydiff, ydiffstd)
    plt.title(cat+", \nvariance: "+str(variance))
    
    cat_trimmed = cat.replace("/", "_")
    plt.savefig(measured_statistic+"for_file_"+cat_trimmed+".png")
    plt.close()
