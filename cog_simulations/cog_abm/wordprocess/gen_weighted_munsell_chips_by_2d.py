'''
Created on Sep 3, 2013

@author: mlukasik
'''
from utils import load_clab, load_position2coordinates, load_coordinates2position,\
for_each_chip, print_munsell_chip, get_borders_position2coordinates
import matplotlib.pyplot as plt
from scipy import matrix
from params import *

if __name__ == "__main__":
	"""import sys
	if len(sys.argv) < 2:
		print "1. parameter: how many times frequent points are going to be multiplied."
		sys.exit(1)
	freq = int(sys.argv[1])
	if len(sys.argv) < 3:
		print "2. parameter: path to xml file with Munsell chips."
		sys.exit(1)
	munsell_fname = sys.argv[2]
	if len(sys.argv) < 4:
		print "3. parameter: path to a c-lab file."
		sys.exit(1)
	clab_fname = sys.argv[3]
	if len(sys.argv) < 5:
		print "4. parameter: path to a chip.txt file."
		sys.exit(1)
	chip_fname = sys.argv[4]
	if len(sys.argv) < 6:
		print "5. parameter: path to a result Munsell chips file."
		sys.exit(1)
	out_fname = sys.argv[5]
	if len(sys.argv) < 7:
		print "6. parameter: path to a 2d picture of result Munsell chips file."
		sys.exit(1)
	out_picname = sys.argv[6]"""

	fout = open(out_fname, 'w')

	clab = load_clab(open(clab_fname, 'r').readlines())
	position2coordinates = load_position2coordinates(chip_fname)
	min_x, max_x, min_y, max_y = get_borders_position2coordinates(position2coordinates)
	print "min_x:", min_x
	print "max_x:", max_x
	print "min_y:", min_y
	print "max_y:", max_y
	coordinates2position = load_coordinates2position(chip_fname)
	
	#matrix for visualization
	range_y = max_y-min_y+1
	print "range_y:", range_y
	range_x = max_x-min_x+1
	print "range_x:", range_x
	mtx = [[0 for _ in xrange(range_y)] for _ in xrange(range_x)]
	
	fout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
	fout.write("<environment type=\"CIELab\">\n")
	
	for ind, munsell_coordinates in enumerate(for_each_chip(open(munsell_fname, 'r'))):
		print_munsell_chip(munsell_coordinates, fout)
		x, y = position2coordinates[ind+1]
		if is_to_be_multiplied(x, y):
			for _ in xrange(freq-1):
				print_munsell_chip(munsell_coordinates, fout)
			mtx[x][y] = freq
		
	fout.write("</environment>\n")
	
	fout.close()
	plt.imshow(matrix(mtx))#, cmap=plt.cm.gray) #Needs to be in row,col order
	plt.savefig(out_picname, bbox_inches='tight')