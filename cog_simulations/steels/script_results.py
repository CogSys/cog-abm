import os
for i in xrange(20):
 
 # os.system("python steels_main.py -s ../../examples/simulations/sim2.json -r  ../../results_of_simulation/results_proba"+format(i)),

     
#  os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_max_max_clos"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_max_max_clos_CSA"+format(i)+".txt"),
#   os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_max_max_clos"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_max_max_clos_DSA"+format(i)+".txt"),
    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_ring"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_ring_CSA"+format(i)+".txt"),
    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_ring"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_ring_DSA"+format(i)+".txt"),
  
    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_clique"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_clique_CSA"+format(i)+".txt"),
    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_clique"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_clique_DSA"+format(i)+".txt")
        
    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_line"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_line_CSA"+format(i)+".txt"),
    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_line"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_line_DSA"+format(i)+".txt")
#
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_max_max_clos"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_max_max_clos_CSA"+format(i)+".txt"),
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_max_max_clos"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_max_max_clos_DSA"+format(i)+".txt")
#
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_max_var_cons"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_max_var_cons_CSA"+format(i)+".txt"),
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_max_var_cons"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_max_var_cons_DSA"+format(i)+".txt")
#
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_min_avg_bet"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_min_avg_bet_CSA"+format(i)+".txt"),
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_min_avg_bet"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_min_avg_bet_DSA"+format(i)+".txt")
#
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_min_avg_clust"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_min_avg_clust_CSA"+format(i)+".txt"),
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_min_avg_clust"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_min_avg_clust_DSA"+format(i)+".txt")
#
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_min_max_clos"+format(i)+" it CSA > ../../results_of_simulation/data_no_shift_sim/data_min_max_clos_CSA"+format(i)+".txt"),
#    os.system("python2 analyzer.py -r ../../results_of_simulation/no_shift_sim/results_min_max_clos"+format(i)+" it DSA > ../../results_of_simulation/data_no_shift_sim/data_min_max_clos_DSA"+format(i)+".txt")





