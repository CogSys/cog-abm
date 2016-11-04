def generate_clique_topology(agents_names):
    """
    Generates clique.

    :param list agents_names: the names of agent that will be used to name all nodes.

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    topology = {}

    for agent_name in agents_names:
        list_without_agent = [name for name in agents_names if not (name == agent_name)]
        topology[agent_name] = list_without_agent

    return topology


def generate_hub_topology(agents_names):
    """
    Generates hub.

    :param list agents_names: the names of agent that will be used to name all nodes.

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    topology = {}

    hub_agent_name = agents_names[0]
    list_without_hub = [name for name in agents_names if not (name == hub_agent_name)]

    topology[hub_agent_name] = list_without_hub
    for agent_name in list_without_hub:
        topology[agent_name] = [hub_agent_name]

    return topology


def generate_line_topology(agents_names):
    """
    Generates line.

    :param list agents_names: the names of agent that will be used to name all nodes.

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    topology = {}

    for i in range(len(agents_names)):
        neighbours = []
        if not (i == 0):
            neighbours.append(agents_names[i - 1])
        if not (i == len(agents_names) - 1):
            neighbours.append(agents_names[i + 1])
        topology[agents_names[i]] = neighbours

    return topology


def generate_ring_topology(agents_names):
    """
    Generates ring.

    :param list agents_names: the names of agent that will be used to name all nodes.

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    topology = generate_line_topology(agents_names)

    last_index = len(agents_names) - 1

    topology[agents_names[0]].append(agents_names[last_index])
    topology[agents_names[last_index]].append(agents_names[0])

    return topology


def generate_standard_topology(topology_type, agents_names=None, agents_number=None):
    """
    Generates topology of given type ("clique", "line", "ring", "hub").

    :param string topology_type: the type of topology to be created.
    :param list agents_names: the names of agent that will be used to name all nodes.
    :param long agents_number: the number of agents for which the topology is created. (Used if agents_names = None.)

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    if agents_names is None:
        agents_names = range(agents_number)

    return {"clique": generate_clique_topology(agents_names),
            "line": generate_line_topology(agents_names),
            "ring": generate_ring_topology(agents_names),
            "hub": generate_hub_topology(agents_names)}[topology_type]


def generate_topology(topology_type, file_name=None, agents_names=None, agents_number=None):
    """
    Generates or load topology of given type ("clique", "line", "ring", "hub", "file").

    :param string topology_type: the type of topology to be created.
    :param string file_name: path to saved topology file. (If "file" topology_type was selected.)
    :param list agents_names: the names of agent that will be used to name all nodes. \
        (If "file" topology_type wasn't selected.)
    :param long agents_number: the number of agents for which the topology is created. (Used if agents_names = None.)

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    if topology_type == "file":
        return read_topology_from_file(file_name)
    else:
        return generate_standard_topology(topology_type, agents_names, agents_number)


def read_topology_from_file(file_name):
    """
    Read saved topology.

    :param string file_name: Path to saved topology file.

    :return: dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    :rtype: dictionary
    """
    import json
    with open(file_name, 'r') as f:
        return json.loads(f.read())
