#!/bin/bash
#calls a simulation steels_main.py and moves results to a specified catalogue
# argument 1: xml wejsciowy z opisem parametrow symulacji (w tym algorytm ML)
# argument 2: katalog z wynikami
mkdir -p $2

START=$(date +%s)
for i in 1
do
	mkdir -p $2/
	python steels_main.py -p $1;
	mv *words.pout $2/
done

