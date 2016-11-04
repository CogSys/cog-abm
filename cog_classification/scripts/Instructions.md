## raw run

You can start testing steels classifier by typing:

python raw_run.py options

###### Options application

* aplha: "-a value"; value - any number from 0 to 1; if not specified value = 0.99;
* good agent measure: "-g value"; value - any number from 0 to 1; if not specified value = 0.95;
* role model: "-r name"; name - RANDON, SPEAKER or HEARER; if not specified name = RANDOM;
* iteration number: "-i value"; value integer from 1; if not specified value = 1000;
* topology: "-t name"; name - clique, line, hub, ring; if not specified name = clique;
* classifiers: "-c name1 name2 ..."; name - Knn1 or Tree; if not specified name1 = Knn1, name2 = Knn1;
* data: "-d name"; name - name of data set (currently available - iris, digits) or path to file with data (if flag data was set); if not specified name = iris;
* output file: "-o path"; path - path to the file in which results should be saved; if not specified path = results;
* data file: "-f"
* zubek type: "-z"
* smart path: "-s"

###### Options description

You can set a lot of custom values that will change classifier behavior:

* alpha - the value responsible for the pace of agent forgetting. The value ranges from 0 (total sclerosis) to 1 (perfect memory). Alpha works by multiplying weights in sample storage by themselves. If sample weight is lower than 0.05 then sample is forgotten. If category has no samples then category is forgotten, too.
* good agent measure - the value responsible for the frequency of new category creation. The value ranges from 0 (create new category ar rarely as possible) to 1 (always create new categories). The new category will be created when agent fails in discrimination game inside guessing game or when hearer doesn't match word with topic and in last 50 guessing games of agent, agent's success in discrimination game was lower than good agent measure.
* role model - the way of assigning agents to roles in games. The agents are chosen to game randomly but the procedure of choosing can influence the probability of assigning certain role to certain agent. To chose two agent first random agent is chosen (every agent has the same probability of being chosen), and then one agent form agents which can communicate with first agent. The default role model is RANDOM - the roles of agents are randomly assigned to them and both agents have the same probability of becoming speaker of hearer. There are two other role models that specifies exactly role of first agent (by what the role of second agent is described too) - SPEAKER and HEARER. If every node in topology has the same degree then the consequences of all three role models are the same. If there are different degrees in topology then role model RANDOM provides the same probability of both roles for every agent. If the role of first agent is specified then agents with lower degree has higher chance of playing this role than players with higher degree.
* iteration number - the number of games that will be played in whole population when fit function will be used.
* topology - the topology name. Topology specifies which agents can interact with each others. You can use clique, line, ring and hub.
* classifiers - the classifiers names. An agent is created for every given classifier name. The currently available names: Knn1 - k nearest neighbours and Tree - decision tree.
* data - name of data set that will be used to create samples on which classifier will be fitted and tested.
* data file - flag that will inform that the name given in data is a path to file with data saved in JSON.
* zubek type - flag that will inform about the other format of saved file.
* smart path - flag that will add "../../data/classification_data/" before the name specified in data
* output file - the path to file in which results of test should be saved. File hasn't to exist before, but any directory on the path has to.

###### Results

The results of simulation are saved in file in JSON format as dictionary. I present structure of dictionary in format:
 
 * key - value
 
 If value is a dictionary or other data structure that store something else then I use nested list:
 
 * key - dictionary1
    * dictionary1_key - list
        * description of the list element
        
 The structure of this dictionary is like following:

* "parameters" - parameters of given classifier test (dictionary)
    * "classifiers" - list of classifiers names (list of strings)
    * "steels" - dictionary
        * "alpha" - alpha value (float)
        * "good_agent_measure" - good agent measure value (float)
        * "role_model" - name of role modes (string)
        * "iteration_number" - number of iterations (int)
        * "topology" - topology name (string)
    * "data" - dictionary
        * "label" - name of data set or path to file with data
* "agents" - list of agents attributes (list of dictionaries)
    * single dictionary
        * "id" - agent id
        * "lexicon_words" - dictionary of words {word: {category: weight}}
            * word - dictionary associated with word
                * category - the weight of association between word and category
        * "lexicon_categories" - dictionary of categories {category: [words]}
            * category - list of words
        * "sample_categories" - dictionary of categories {category: {environment: ([sample_indexes, sample_weight])}}
            * category - dictionary of environments
                * environment - tuple
                    * list of sample indexes
                    * list of weights (sample - category weight)
        * "sample_classes" - dictionary of categories
            * category - number of class
        * "CS" - communicative success (float)
        * "DS" - discriminative success (float)
* "accuracy" - the accuracy of steels classifier tested on 1/3 of data (training on 2/3 of rest)

######  Attention

Both environment and class are represented by integers. Their representation is constant inside one test (in every agent description environment 2 means the same) but between tests the same environment can have two different number representation.

The categories are inner construct of agent so "Category: 0" in one agent doesn't correspond to "Category: 0" in other agent.

### Possible extension

There are quite few things that can be added rather easy with writing only a few lines of code.
 
###### New classifiers

First - the classifier that you want to add should implement standard sklearn classifiers methods:

* predict
* fit
* predict_proba

Classifier should work for set of samples with size 2 or bigger.

Second - raw_run changes:

* import your classifier - example - "from cog_classification.steels.steels_classifier import NewSteelsClassifier"
* change method make_classifier - add to dictionary after return - "name_of_classifier": NewSteelsClassifier(all needed parameters)

Third - change this file and add your classifier name to this file description and application of options.

###### New topologies

First - change topology_generator.py file in tools directory:

* add method that generates topology for given array of agents names
* add name of your topology to generate standard topology dictionary after return - example - "wheel": generate_wheel_topology(agent_names)

Second - change this file and add your topology name to this file description and application of options.

### run

Inside the raw_run script there is a method run that can be used in separation. Run takes one argument: dictionary. The structure of this dictionary:

* "classifiers" - the list of names of classifiers
* "steels" - dictionary
    * "alpha" - alpha value (float)
    * "good_agent_measure" - good agent measure value (float)
    * "role_model" - name of role modes (string)
    * "iteration_number" - number of iterations (int)
    * "topology" - topology name (string)
* "data" - the tuple
    * samples - list of vectors of sample's features
    * classes - list of sample's classes

The run function returns dictionary with the following structure:

* "agents" - list of agents attributes (list of dictionaries)
    * single dictionary
        * "id" - agent id
        * "lexicon_words" - dictionary of words {word: {category: weight}}
            * word - dictionary associated with word
                * category - the weight of association between word and category
        * "lexicon_categories" - dictionary of categories {category: [words]}
            * category - list of words
        * "sample_categories" - dictionary of categories {category: {environment: ([sample_indexes, sample_weight])}}
            * category - dictionary of environments
                * environment - tuple
                    * list of sample indexes
                    * list of weights (sample - category weight)
        * "sample_classes" - dictionary of categories
            * category - number of class
        * "CS" - communicative success (float)
        * "DS" - discriminative success (float)
* "accuracy" - the accuracy of steels classifier tested on 1/3 of data (training on 2/3 of rest)

## advanced run

The advanced run is script that uses set of hard coded levels variables to create experiments that uses all combinations of this levels.

 Results of this script are saved in file results_of_steels_classifier.json in the folder of script execution. The results are saved in JSON format as a dictionary with structure:

* "all_levels":
    * "classifiers" - list of list of classifiers names (list of strings)
    * "alpha" - list of alpha values (float)
    * "good_agent_measure" - list of good agent measure values (float)
    * "role_model" - list of names of role modes (string)
    * "iteration_number" - list of numbers of iterations (int)
    * "topology" - list of topology names (string)
    * "data" - list of names of zubek data files (string)
* "simulations" - list of dictionaries with structure:
    * "parameters" - parameters of given classifier test (dictionary)
        * "classifiers" - list of classifiers names (list of strings)
        * "alpha" - alpha value (float)
        * "good_agent_measure" - good agent measure value (float)
        * "role_model" - name of role modes (string)
        * "iteration_number" - number of iterations (int)
        * "topology" - topology name (string)
        * "data" - dictionary
            * "label" - name of data set or path to file with data
    * results - list of results of repetitive testing with constant parameters; the result is identical with the dictionary returned by method run.
    