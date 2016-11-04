import argparse
import json

import sys
sys.path.append('../../')
sys.path.append('../')
sys.path.append('')

import pandas as pd
import numpy as np

from sklearn import tree
from sklearn import neighbors

from sklearn import datasets

from cog_classification.steels.steels_classifier import SteelsClassifierExtended


def add_arguments(new_parser):

    new_parser.add_argument('-a', '--alpha', dest='alpha', default=0.99, type=float, action='store')

    new_parser.add_argument('-g', '--good_agent_measure', dest='good_agent_measure', default=0.95, type=float,
                            action='store')

    new_parser.add_argument('-r', '--role_model', dest='role_model', default="RANDOM", type=str, action='store')

    new_parser.add_argument('-i', '--iteration_number', dest='iteration_number', default=1000, type=int, action='store')

    new_parser.add_argument('-t', '--topology', dest='topology', default="clique", type=str, action='store')

    new_parser.add_argument('-c', '--classifiers', dest='classifiers', default=["Knn1", "Knn1"], type=str, nargs='*',
                            action='store')

    new_parser.add_argument('-d', '--data', dest='data', default="iris", type=str, action='store')

    new_parser.add_argument('-f', '--data_file', dest='data_file', action='store_true')

    new_parser.add_argument('-z', '--zubek_type', dest='zubek_type', action='store_true')

    new_parser.add_argument('-s', '--smart_path', dest='smart_path', action='store_true')

    new_parser.add_argument('-o', '--output_file', dest='output_file', default="results", type=str,
                            action='store')


def run(data):
    """
    Creates and runs classifier described in data for samples defined in data.

    :param data: dictionary with all parameters needed to make classifier and data.
    :type data: dictionary

    :return: * the result of the classifier. *(dictionary)*
            * the data described classifier and data. *(dictionary)*
    """

    # Making classifiers for SteelsClassifier.
    single_classifiers = [make_classifier(name) for name in data["classifiers"]]

    # Reading all SteelsClassifier statistics on variable.
    steels = data["steels"]

    # Making SteelsClassifier.
    classifier = SteelsClassifierExtended(classifiers=single_classifiers,
                                          alpha=steels["alpha"],
                                          good_agent_measure=steels["good_agent_measure"],
                                          role_model=steels["role_model"],
                                          iteration_number=steels["iteration_number"],
                                          topology=steels["topology"])

    samples, classes = data["data"]
    return classifier.get_results(samples, classes)


def make_classifier(classifier_name):
    """
    Creates classifier with given name.

    :param string classifier_name: the name of classifier.

    :return: the created classifier.
    :rtype: classifier
    """

    return {"Tree": tree.DecisionTreeClassifier(),
            "Knn1": neighbors.KNeighborsClassifier(n_neighbors=1)
            }.get(classifier_name)


def read_data(information):
    """
    Reads described data.

    :param information: the dictionary with data parameters.
    :type information: dictionary

    :return: two arrays - with samples and classes of samples
    :rtype: tuple
    """

    if information["type"] == "name":

        # Loading data.
        data = {"iris": datasets.load_iris(),
                "digits": datasets.load_digits()
                }.get(information["name"])

        # Setting string describing data.
        information["label"] = information["name"]

        return data["data"], data["target"]

    else:
        file_path = information["path"]

        if information["find"] == "smart":
            file_path = "../../data/classification_data/" + file_path

        # Setting string describing data.
        information["label"] = information["path"]

        if information["type"] == "zubek":

            # Loading data.
            return load_data_set(file_path)

        else:

            return json.load(file_path)


def load_data_set(filename):
    """
    Loads a data set from UCI file. All non-numerical columns are factorized.
    Optional auxiliary file contains list of columns not used in machine
    learning. First index on the list should point class column. If auxiliary
    file is not present, the last column is treated as class.

    :returns: * x -- matrix containing values of all attributes.
        * y -- vector containing class values.

    Method from https://bitbucket.org/zubekj/selection_ensembles.
    """
    try:
        with open('{0}.class'.format(filename)) as f:
            columns_to_skip = [int(c) for c in f.readline().split(" ")]
    except (IOError, ValueError):
        columns_to_skip = [-1]

    df = pd.read_csv(filename, header=None)
    x = [pd.factorize(df[col])[0] if df[col].dtype.kind == 'O' else df[col] for col in df]

    y = np.array(x[columns_to_skip[0]])
    x = [f for i, f in enumerate(x) if not (i in columns_to_skip or (i-len(x)) in columns_to_skip)]

    return np.array(x, dtype=float).T, y


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program is implementation of Steels classifier.")
    add_arguments(parser)
    args = parser.parse_args()

    data_parameters = {"label": args.data}

    if args.data_file:

        data_parameters["path"] = args.data

        if args.smart_path:
            data_parameters["find"] = "smart"
        else:
            data_parameters["find"] = "normal"

        if args.zubek_type:
            data_parameters["type"] = "zubek"
        else:
            data_parameters["type"] = "normal"

    else:
        data_parameters["name"] = args.data

    parameters = {"classifiers": args.classifiers,
                  "steels": {
                      "alpha": args.alpha,
                      "good_agent_measure": args.good_agent_measure,
                      "role_model": args.role_model,
                      "iteration_number": args.iteration_number,
                      "topology": args.topology
                  },
                  "data": data_parameters}

    output_parameters = parameters.copy()

    parameters["data"] = read_data(parameters["data"])

    results = run(parameters)
    results["parameters"] = output_parameters

    with open(args.output_file, 'w') as f:
        json.dump(results, f)
