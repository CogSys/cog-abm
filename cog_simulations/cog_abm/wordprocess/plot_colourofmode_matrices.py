'''

Created on Sep 01, 2013

@author: mlukasik

Plot intensity matrices depicting modes. 
'''
from utils import string2prefix_num, get_files, get_modacolor_dict, load_position2coordinates,\
 ensure_dir, get_borders_position2coordinates, convert_modacolor_to_naturals, rescale
from scipy import matrix
import scipy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from params import *
if __name__ == "__main__":
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
        word_modacolor = get_modacolor_dict(cat, fname)
        print "word_modacolor:", word_modacolor
        word_modacolor = convert_modacolor_to_naturals(word_modacolor)
        print "word_modacolor:", word_modacolor
        #mtx = [[0]*(max_y-min_y+1)]*(max_x-min_x+1) VERY WRONG!! CHECK WHY
        mtx = [[0 for _ in xrange(max_y-min_y+1)] for _ in xrange(max_x-min_x+1)]
        for key, moda in word_modacolor.iteritems():
            x, y = position2coordinates[key+1]
            mtx[x][y] = moda
        
        mtx = rescale(mtx, 10)
        
        #print matrix(mtx)
        #matrices[string2prefix_num(fname)] = ...
        #scipy.misc.imsave(str(string2prefix_num(fname))+'.jpg', matrix(mtx))
        ax = plt.gca()
        ax.patch.set_alpha(0.0)
        
        xtick_locs = [0, 20, 40, 60, 80]
        xtick_labels = [0, 2, 4, 6, 8]
        plt.yticks(xtick_locs, xtick_labels)
        ytick_locs = [0, 100, 200, 300, 400]
        ytick_labels = [0, 10, 20, 30, 40]
        plt.xticks(ytick_locs, ytick_labels)
        
        img = plt.imshow(matrix(mtx))#, cmap=cm.Greys_r) #Needs to be in row,col order
        
        # make a color bar
        plt.colorbar(img)
        #plt.clim(0,8)
        plt.savefig(res_cat+str(string2prefix_num(fname))+'.jpg', bbox_inches='tight')
        plt.close()

