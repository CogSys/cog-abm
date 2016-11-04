import json

from raw_run import load_data_set, run


if __name__ == "__main__":

    agents_numbers = [2, 4, 8, 16]
    k = "Knn1"
    t = "Tree"
    classifiers = []
    for n in agents_numbers:
        classifiers.extend([[k for _ in range(n)],
                            [t for _ in range(n)]])
    role_models = ["RANDOM",
                   "SPEAKER",
                   "HEARER"]
    topology = ["clique",
                "hub",
                "line",
                "ring"]
    iteration_numbers = [1000, 2000, 4000, 8000, 16000]
    alphas = [0.01 * x for x in range(11)]
    good_agent_measures = [0.01 * x for x in range(11)]

    data = ["colon.csv",
            "glass.data",
            "handwriting.csv",
            "leukemia.csv",
            "prostate.csv"]

    all_data = []
    for d in data:
        source = load_data_set("../../data/classification_data/"+d)
        for c in classifiers:
            for r in role_models:
                for t in topology:
                    for it in iteration_numbers:
                        for a in alphas:
                            for g in good_agent_measures:
                                parameters = {"classifiers": c,
                                              "steels": {
                                                  "alpha": a,
                                                  "good_agent_measure": g,
                                                  "role_model": r,
                                                  "iteration_number": it,
                                                  "topology": t
                                              },
                                              "data": source}
                                results = []
                                for rep in range(20):
                                    results.append(run(parameters))

                                parameters["data"] = d
                                all_data.append({"parameters": parameters,
                                                 "results": results})

    raport = {"simulations": all_data}
    levels = {"classifiers": classifiers,
              "alpha": alphas,
              "good_agent_measure": good_agent_measures,
              "role_model": role_models,
              "iteration_number": iteration_numbers,
              "topology": topology,
              "data": data}
    raport["all_levels"] = levels

    with open("results_of_steels_classifier.json", "w") as f:
        json.dump(raport, f)
