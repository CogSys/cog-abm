#!/bin/bash
#generates simulation results, repeated multiple times
# argument 1: number of simulation repetitions
# argument 2: path to simulation.xml
#argument 3: output catalogue
for i in $(seq 0 $1)
do
    sh ./call_simulation_move_results.sh $2 $3"/results_"$1"_"$i
done
