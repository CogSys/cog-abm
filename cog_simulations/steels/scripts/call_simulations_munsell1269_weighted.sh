#!/bin/bash
# argument 1: suffix nazwy symulacji, np a_larger
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
	sh ./call_simulation_move_results.sh "../../data/1269_munsell_chips_weighted_simulation_xmls/simulation_artificial_"$1".xml" "wcs_1269_"$1""$i
done

