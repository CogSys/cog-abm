'''
Created on Jan 2, 2013

@author: mlukasik
'''
from utils import traverse_clab_file, get_median_in_clab,\
for_each_chip, print_munsell_chip

def is_to_be_multiplied(point, coordinate, side, mid_pnt):
	'''Checks if the conditions to be multipled are fulfilled.
	'''
	if side == "less":
		if point[coordinate] < mid_pnt:
			return True
		else:
			return False
	elif side == "larger":
		if point[coordinate] >= mid_pnt:
			return True
		else:
			return False
	else:
		print "ERROR: wrong argument for side parameter: should be less or larger, whereas passed: ", side

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print "1. parameter: coordinate according to which a splitting is done."
		sys.exit(1)
	coordinate = int(sys.argv[1])
	if len(sys.argv) < 3:
		print "2. parameter: which half is going to be multiplied: less or larger."
		sys.exit(1)
	side = sys.argv[2]
	if len(sys.argv) < 4:
		print "3. parameter: how many time one half is going to be multiplied."
		sys.exit(1)
	freq = int(sys.argv[3])
	if len(sys.argv) < 5:
		print "4. parameter: path to xml file with Munsell chips."
		sys.exit(1)
	fname = sys.argv[4]
	if len(sys.argv) < 6:
		print "5. parameter: path to a c-lab file."
		sys.exit(1)
	clab = sys.argv[5]

	mid_pnt = get_median_in_clab( traverse_clab_file(open(clab, 'r')), coordinate)

	print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
	print "<environment type=\"CIELab\">"
	
	for x, y, z in for_each_chip(open(fname, 'r')):
		print_munsell_chip((x, y, z))
		if is_to_be_multiplied((x, y, z), coordinate, side, mid_pnt):
			for _ in xrange(freq-1):
				print_munsell_chip((x, y, z))
	
	print "</environment>"
