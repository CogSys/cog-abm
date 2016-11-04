'''

Created on Jan 2, 2013

@author: mlukasik

Module with functions for analysis of output file from simulation with words.

File with words is of the following form:
agent-no1 list-of-words
agent-no2 list-of-words
.
.
.


'''
from __future__ import division
from collections import defaultdict

def read_words(f):
	'''
	Read words as saved by the steels simulation.
	
	Create a dictionary: agent -> list of words
	'''
	words_per_agent = {}
	for ind, line in enumerate(f):
		words_per_agent[ind] = line.split()[1:]
	return words_per_agent

def is_number(s):
	'''
	@type s - string 
	Checks if s is a number.
	'''
	try:
		float(s)
		return True
	except ValueError:
		return False

def string2prefix_num(s):
	'''
	Maps s into an integer corresponding iteration number. This is done basing
	on naming of results of simulation.
	>>> string2prefix_num("0words.pout")
	0
	>>> string2prefix_num("1000words.pout")
	1000
	>>> string2prefix_num("10000words.pout")
	10000
	'''
	if not is_number(s[1]):
		return int(s[0])
	if not is_number(s[4]):
		return int(s[:4])
	return int(s[:5])

def get_word_count(words_per_agent, nullify = True):
	'''
	For each position in the words list, calculate how many times each word occurs.
	'''
	word_count = defaultdict(lambda: {})
	
	for words in words_per_agent.itervalues():
		for ind, word in enumerate(words):
			if word not in word_count[ind]:
				word_count[ind][word] = 1
			else:
				word_count[ind][word] += 1
	
	#force -1's count to be 0 - we exclude it from further analysis
	if nullify:
		for ind in word_count.iterkeys():
			word_count[ind][-1] = 0
			word_count[ind]['-1'] = 0
	
	return dict(word_count)

def read_clab_splitted_by_median(lines, coordinate):
	'''
	Return 2 subsets of colours, divided by the median of values for a given
	coordinate.
	'''
	median = get_median_in_clab(lines, coordinate)
	bigger, smaller = read_clab_splitted_into_2(lines, coordinate, median)
	return bigger, smaller

def get_median_in_clab(lines, coordinate):
	'''
	Find a median in terms of values for a given coordinate.
	
	lines - lines of a c-lab file, where coordinates start from 6th column
	 onwards. Therefore, the coordinate parameter is added to 6 when 
	 extracting values.
	'''
	elems = []
	for _, colour in lines:
		elems.append(colour[coordinate] )
	import numpy
	mid_pnt = numpy.median(elems)
	return mid_pnt

def read_clab_splitted_into_2(lines, coordinate, splitting_point):
	'''
	Read the c-lab data by splitting it into 2 subsets: elements larger
	with respected to coordinate then the given splitting_point, 
	and elements smaller then the splitting_point.
	'''
	bigger = set()
	smaller = set()
	
	for index, colour in lines:
		v = colour[coordinate]
		if v >= splitting_point:
			bigger.add(index)
		else:
			smaller.add(index)
	return bigger, smaller

def calculate_moda(elements):
	'''
	Calculates what percentage the biggest element contributes.
	
	>>> calculate_moda( [5, 5, 5, 5] )
	0.25
	>>> calculate_moda( [0, 10] )
	1.0
	>>> calculate_moda( [1, 2, 1] )
	0.5
	>>> calculate_moda( [0] )
	0
	'''
	moda = 0
	all_occurences = sum(elements)
	if all_occurences != 0:
		moda = max(elements)*1.0/sum(elements)
	return moda

def get_moda_fraction_list_per_set(word_count, set1, set2):
	'''
	word_count - maps a position, to a dictionary, which in turn maps each word
	to occurence count
	
	For each position in set1 and set2, return what percentage the most common
		word contributes.
	'''
	moda_for_set1 = []
	moda_for_set2 = []
	for index, words in word_count.iteritems():
		#calculate moda:
		moda = calculate_moda(list(words.itervalues()))
		if index in set1:
			moda_for_set1.append(moda)
		elif index in set2:
			moda_for_set2.append(moda)
		else:
			print "[get_moda_fraction_list_per_set ] ERROR, index in none of the sets", index
			exit(1)
	return moda_for_set1, moda_for_set2

def avg_num_of_words_per_agent_for_sets(words_per_agent, set1, set2):
	'''
	For each set find number of distinct words per index.
	'''
	
	agent_distinctwords_set1 = defaultdict(lambda: set())
	agent_distinctwords_set2 = defaultdict(lambda: set())
	
	for words in words_per_agent.itervalues():
		#print "words:", words
		for ind, word in enumerate(words):
			if ind in set1:
				agent_distinctwords_set1[ind].add(word)
			elif ind in set2:
				agent_distinctwords_set2[ind].add(word)
			else:
				print "[find_num_of_words_per_agent_per_set] ERROR, ind in none of the sets", ind
				exit(1)
	
	def calculate_avg_words(agent_distinctwords_set):
		lengths = map(lambda x: len(x), agent_distinctwords_set.itervalues())
		return sum(lengths)*1.0/len(lengths)
	
	avg_bigger = calculate_avg_words(agent_distinctwords_set1)
	avg_smaller = calculate_avg_words(agent_distinctwords_set2)
	return avg_bigger, avg_smaller
	
def traverse_clab_file(lines):
	'''
	Yield each consecutive: index (starting from 0) + coordinates of a point.
	'''
	for line in lines:
		splitted = line.split()
		yield int(splitted[0]) - 1, (float(splitted[6]), float(splitted[7]), float(splitted[8]))

def load_clab(lines):
	clab = {}
	for pos, (L, a, b) in traverse_clab_file(lines):
		clab[pos] = (L, a, b)
	return clab

def load_position2coordinates(chip_fname):
	'''
	Returns: position2coordinates - mapping from position of a colour in result file to its coordinates
		in 2d plane.
	'''
	position2coordinates = {}
	for l in open(chip_fname, 'U').xreadlines():
		pos, x, y, _ = l.split()
		position2coordinates[int(pos)] = (ord(x)-ord('A'), int(y))
	return position2coordinates

def load_coordinates2position(chip_fname):
	'''
	Returns: coordinates2position - mapping from coordinates
		in 2d plane to position of a colour in result file.
	'''
	coordinates2position = {}
	for l in open(chip_fname, 'U').xreadlines():
		pos, x, y, _ = l.split()
		coordinates2position[(ord(x)-ord('A'), int(y))] = int(pos) 
	return coordinates2position

def get_borders_position2coordinates(position2coordinates):
	'''
	Returns borders of coordinates.
	'''
	min_x = min(map(lambda (x, y): x, position2coordinates.itervalues()))
	max_x = max(map(lambda (x, y): x, position2coordinates.itervalues()))
	min_y = min(map(lambda (x, y): y, position2coordinates.itervalues()))
	max_y = max(map(lambda (x, y): y, position2coordinates.itervalues()))
	return min_x, max_x, min_y, max_y


def get_mode_word_stats(fname, clab_fname, coordinate):
	'''
	fname - path to a file with words saved.
	clab_fname - path to a c-lab file.
	coordinate - according to which coordinate we perform split in analysis.
	'''
	words_per_agent = read_words(open(fname, 'r'))
	bigger, smaller = read_clab_splitted_by_median(
						list(traverse_clab_file(open(clab_fname, 'r'))),
						coordinate)
	
	avg_wordnum1, avg_wordnum2 = \
		avg_num_of_words_per_agent_for_sets(words_per_agent, bigger, smaller)
	
	word_count = get_word_count(words_per_agent)
	moda_bigger, moda_smaller = get_moda_fraction_list_per_set(word_count, bigger, smaller)
	avg_moda_bigger = sum(moda_bigger)*1.0/len(moda_bigger)
	avg_moda_smaller = sum(moda_smaller)*1.0/len(moda_smaller)
	return avg_moda_bigger, avg_moda_smaller, avg_wordnum1, avg_wordnum2
	
#===============================WORD GENERATING===============================#
def get_numerical(line):
	'''
	Extracts a numerical value from inside of xml line.
	'''
	return float(line.split('>')[1].split("<")[0])

def for_each_chip(f):
	'''
	For each munsell chip found in f, yields numerical values of its coordinates.
	'''
	while True:
		l = f.readline()
		if not l:
			break
		if "<munsell_chip>" in l:
			x = get_numerical(f.readline())
			y = get_numerical(f.readline())
			z = get_numerical(f.readline())
			if "</munsell_chip>" not in f.readline():#closing of munsell_chip
				print "[for_each_chip] ERROR! no closing of munsell_chip found"
			yield x, y, z

#############################################################################################################

import os
def get_nested_catalogues(cat):
	'''
		Returns: cats - catalogues from cat
	'''
	cats = map(lambda x: cat+"//"+x, os.listdir(cat))
	return cats
	

def get_files(cat):
	'''
		Returns: files - ids of consecutive time stamps, used in statistics dictionary
	'''
	#assume that in each catalogue there are files named the same, which correspond to one another
	cats = get_nested_catalogues(cat)
	files = os.listdir(cats[0])
	return files

def get_moda_dict(arg_cat, fname):
	'''
	Returns: word_moda - dictionary mapping each colour to moda value.
	'''
	cats = get_nested_catalogues(arg_cat)
	
	word_moda = {}
	for cat in cats:
		#read list of words per each color 
		words_per_agent = read_words(open(cat+"/"+fname, 'r'))
		#counts of words per each color
		word_count = get_word_count(words_per_agent)
		#convert to maximum, adding at once which corresponds to taking average
		for key, item in word_count.iteritems():
			word_moda[key] = word_moda.get(key, 0) + max(item.itervalues())
	for key in word_moda.iterkeys():
		word_moda[key] /= len(cats)
	
	return word_moda

def get_modacolor_dict(arg_cat, fname):
	'''
	Returns: word_modacolor - dictionary mapping each colour to its name taken from moda.
	'''
	cats = get_nested_catalogues(arg_cat)
	
	word_modacolor = {}
	for cat in cats:
		#read list of words per each color 
		words_per_agent = read_words(open(cat+"/"+fname, 'r'))
		#counts of words per each color
		word_count = get_word_count(words_per_agent)
		#find the most frequent colour:
		for key, item in word_count.iteritems():
			highest = 0
			for color, intensity in item.iteritems():
				if intensity > highest:
					word_modacolor[key] = color
	
	return word_modacolor

def convert_modacolor_to_naturals(word_modacolor):
	'''
	Assigns a natural number to each colour.
	'''
	color2natural = {}
	next_natural = 1
	for key in word_modacolor:
		if word_modacolor[key] not in color2natural:
			color2natural[word_modacolor[key]] = next_natural
			next_natural += 1
		word_modacolor[key] = color2natural[word_modacolor[key]]
	return word_modacolor
	
#############################################################################################################

def ensure_dir(f):
	'''
	Ensures that dir f exists, if not then creates it
	'''
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

#############################################################################################################
import sys
def print_munsell_chip(point, fout=sys.stdout):
	'''Prints a point in a Munsell Chip manner.
	'''
	(x, y, z) = point
	fout.write("\t<munsell_chip>\n")
	fout.write("\t\t<L>%f</L>\n" % x)
	fout.write("\t\t<a>%f</a>\n" % y)
	fout.write("\t\t<b>%f</b>\n" % z)
	fout.write("\t</munsell_chip>\n")
	
def rescale(mtx_orig, p):
	'''
	Rescales mtx, printing each cell p times.
	'''
	mtx = [[0 for _ in xrange(p*len(mtx_orig[0]))] for _ in xrange(p*len(mtx_orig))]
	for ri, row in enumerate(mtx_orig):
		for ci, cell in enumerate(row):
			for i in xrange(p): 
				for j in xrange(p):
			 		mtx[p*ri+i][p*ci+j] = cell
	return mtx
	
	
if __name__ == "__main__":
	import doctest
	doctest.testmod()
