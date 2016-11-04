# -*- coding: utf-8 -*-
# /COG_SIM
import os
from multiprocessing import Pool
import pandas as pd # must be python2

N_PROC = 4


networks= ["hub_hearer", "hub_speaker", "env_shift_training_hub_speaker", "env_shift_training_hub_hearer"]
results = {"CSA", "DSA", "CLA", "DG_CLA", "cc"}

pool = Pool(processes=N_PROC)

# simulations
for i in xrange(20):
    for network in networks:
        res_fname = "results_of_simulation/hub_sim_results/results_{0}_to_clique{1}".format(network, i)
        if not os.path.isfile(res_fname):
            pool.apply_async(os.system, ["python2 cog_simulations/steels/steels_main.py -s examples/simulations/hub_simulations/simulation_{0}_to_clique.json -r {1}".format(network, res_fname)])

pool.close()
pool.join()

pool = Pool(processes=N_PROC)

# analyzer
for i in xrange(20):
    for result in results:
        for network in networks:
            res_fname = "results_of_simulation/hub_sim_data/data{0}{2}_{1}".format(network, i, result)
            if not os.path.isfile(res_fname):
                pool.apply_async(os.system, ["python2 cog_simulations/steels/analyzer.py -r results_of_simulation/hub_sim_results/results_{0}_to_clique{1} it {2} > {3}".format(network, i, result, res_fname)])

pool.close()
pool.join()

# pandas

index = range(0, 20010, 50)
columns = []

for result in results:
    columns.append(result + "_mean")
    columns.append(result + "_var")

mindex = pd.MultiIndex.from_product((networks, index))
data = pd.DataFrame(index=mindex, columns=columns)

networks= ["hub_hearer", "hub_speaker"]

for result in results:
    for network in networks:
        mean = pd.DataFrame(index=index)
        var = pd.DataFrame(index=index)
        for i in xrange(20):
            data_sim = pd.read_csv(
                "results_of_simulation/hub_sim_data/data{0}{1}_{2}".format(network, result, i), delim_whitespace=True, header=None, index_col=0)
            mean[i] = (data_sim.mean(1))
            var[i] = (data_sim.var(1))
        data[result + "_mean"][network] = mean.mean(1)
        data[result + "_var"][network] = var.mean(1)

with open("simulations_hub_sim_results.csv", 'w') as f:
    data.to_csv(f)
