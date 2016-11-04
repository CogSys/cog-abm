'''

Created on Sep 01, 2013

@author: mlukasik

Plot intensity matrices depicting modes. 
'''
from utils import string2prefix_num, get_files, get_moda_dict, load_position2coordinates,\
 ensure_dir, get_borders_position2coordinates
from scipy import matrix
import scipy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from params import *
if __name__ == "__main__":
    """import sys
    if len(sys.argv) < 2:
        print "Parameter 1: a file with words in chip format (probably available only for"+\
            " 330 munsell chips, since it is used to map a chip to its 2d coordinates."
        exit(1)
    chip_fname = sys.argv[1]#plik z c-lab
    if len(sys.argv) < 3:
        print "Parameter 2: catalogue, where results of a simulation to be analyzed are stored."
        exit(1)
    cat = sys.argv[2]#katalog z danymi
    if len(sys.argv) < 4:
        print "Parameter 3: catalogue, where pictures resulting from this script are to be stored."
        exit(1)
    res_cat = sys.argv[3]#katalog z wynikami
    print "res_cat:", res_cat
    ensure_dir(res_cat)"""
    
    position2coordinates = load_position2coordinates(chip_fname)
    print "position2coordinates:", position2coordinates 
    min_x, max_x, min_y, max_y = get_borders_position2coordinates(position2coordinates)
    print "min_x:", min_x
    print "max_x:", max_x
    print "min_y:", min_y
    print "max_y:", max_y
    
    files = get_files(cat)
    matrices = {}
    for fname in sorted(files, key=lambda x: string2prefix_num(x)):
        ######################################################################
        #generate results for current fname
        word_moda = get_moda_dict(cat, fname)
        print "word_moda:", word_moda
        
        #mtx = [[0]*(max_y-min_y+1)]*(max_x-min_x+1) VERY WRONG!! CHECK WHY
        mtx = [[0 for _ in xrange(max_y-min_y+1)] for _ in xrange(max_x-min_x+1)]
        for key, moda in word_moda.iteritems():
            x, y = position2coordinates[key+1]
            mtx[x][y] = moda
        #print matrix(mtx)
        #matrices[string2prefix_num(fname)] = ...
        #scipy.misc.imsave(str(string2prefix_num(fname))+'.jpg', matrix(mtx))
        ax = plt.gca()
        ax.patch.set_alpha(0.0)
        img = plt.imshow(matrix(mtx))#, cmap=cm.Greys_r) #Needs to be in row,col order
        # make a color bar
        plt.colorbar(img)
        plt.clim(0,8)
        plt.savefig(res_cat+str(string2prefix_num(fname))+'.jpg', bbox_inches='tight')
        plt.close()

