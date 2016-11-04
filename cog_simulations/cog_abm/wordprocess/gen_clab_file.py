'''
Generates c-lab file based on an xml file with chips.
'''
from utils import for_each_chip

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print "Pass an argument: file with Munsell chips."
		sys.exit(1)
	munsell_file = sys.argv[1] #xml file with chips

	cnt = 1
	
	with open(munsell_file, 'r') as f:
		for x, y, z in for_each_chip(f):
			print "%d A A A A A %f %f %f" % (cnt, x, y, z)
			cnt+=1
