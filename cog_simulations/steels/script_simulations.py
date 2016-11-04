import os
for i in xrange(1):{
}
 
 # os.system("python steels_main.py -s ../../examples/simulations/sim2.json -r  ../../results_of_simulation/results_proba"+format(i)),
  
  os.system("python2 analyzer.py -r ../../results_of_simulation/results_proba"+format(i)+" it CSA > results_proba_CSA"+format(i)+".txt"),

  os.system("python2 analyzer.py -r ../../results_of_simulation/results_proba"+format(i)+" it DSA > results_proba_DSA"+format(i)+".txt"),


}