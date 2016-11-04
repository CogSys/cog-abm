import networkx as nx
import topology_generator as gen


size = 16

def write_graph(graph_name, g):
    radius = nx.radius(g)
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.distance_measures.radius.html

    diameter = nx.diameter(g)
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.distance_measures.diameter.html

    closeness = float(sum(nx.algorithms.centrality.closeness_centrality(g).values()))/size
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.centrality.closeness_centrality.html#networkx.algorithms.centrality.closeness_centrality

    betweenness = float(sum(nx.algorithms.centrality.betweenness_centrality(g).values()))/size
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.centrality.betweenness_centrality.html#networkx.algorithms.centrality.betweenness_centrality

    clustering = float(sum(nx.algorithms.clustering(g).values()))/size
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.cluster.clustering.html#networkx.algorithms.cluster.clustering

    print "%s\t%s\t%s\t%s\t%s\t%s" % (graph_name, radius, diameter, closeness, betweenness, clustering)

print("Topology\tRadius\tDiameter\tCloseness\tBetweenness\tClustering")

graphs = ["clique", "line", "hub"]

for graph in graphs:
    g = nx.Graph(gen.generate_topology(graph, agents_names=range(size)))
    write_graph(graph, g)

path = "../../examples/networks/"
files = ["graph_max_avg_bet.json",
         "graph_max_avg_clust.json",
         "graph_max_max_bet.json",
         "graph_max_max_clos.json",
         "graph_max_var_cons.json",
         "graph_min_avg_bet.json",
         "graph_min_avg_clust.json",
         "graph_min_max_clos.json"]

for f in files:
    source = gen.generate_topology("file", file_name=path+f)

    graph = {}

    for node in source["nodes"]:
        graph[node] = []
        for edge in source["edges"]:
            if edge["from"] == node:
                graph[node].append(edge["to"])

    g = nx.Graph(graph)
    write_graph(f, g)