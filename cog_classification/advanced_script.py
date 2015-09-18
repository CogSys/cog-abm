import json

from cog_classification.scripts.run import run

repetition = 10

alpha_min = 0
alpha_max = 1
alpha_step = 0.1

threshold_min = 0
threshold_max = 1
threshold_step = 0.1

classifiers_source = ['class_KNN1_10.json', 'class_DT_10.json']
''', 'class_DT_10.json']'''
classifiers_path = '../examples/'

tasks_source = ['task_glass.json']
''', 'task_colon.json']'''
tasks_path = '../examples/'

results_file = '../results_of_simulation/compare_alpha_threshold'

results = {}
for classifiers in classifiers_source:
    results[classifiers] = {}
    for tasks in tasks_source:
        results[classifiers][tasks] = []

for i in range(int(alpha_min * 100), int((alpha_max + alpha_step) * 100), int(alpha_step * 100)):
    alpha = float(i) / 100
    for j in range(int(threshold_min * 100), int((threshold_max + threshold_step) * 100), int(threshold_step * 100)):
        threshold = float(j) / 100
        for classifiers in classifiers_source:
            for tasks in tasks_source:
                result = []
                for k in xrange(repetition):
                    result.append(run(classifiers_path + classifiers,
                                      tasks_path + tasks,
                                      alpha,
                                      threshold))
                general_results = {"alpha": alpha, "threshold": threshold}

                for statistic in result[0].keys():
                    statistic_sum = 0
                    for r in result:
                        statistic_sum += r[statistic]
                    general_results[statistic] = float(statistic_sum)/len(result)

                results[classifiers][tasks].append(general_results)
        print "Done! Alpha: %s, Threshold: %s" % (alpha, threshold)

with open(results_file, 'w') as f:
    json.dump(results, f)
