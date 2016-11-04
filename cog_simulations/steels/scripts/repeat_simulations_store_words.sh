#!/bin/bash
#argument 1: path to xml describing steels simulation
#argument 2: prefix of cataogue name with results; names are appended by iteration number 
#argument 3: number of repetitions of a simulation
for ((num = 1; num <= $3; num++)); do
	mkdir -p $2'_'$num/
	python steels_main.py -p $1;
	mv *words.pout $2'_'$num/
	rm experiment*
done

