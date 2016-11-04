from pygraph.algorithms.generators import generate
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
import json


def graph_generator(g_type='Clique', n=10, source=None):

    if g_type == "Source":
        return generate_source_graph(source)

    return {"Clique": generate_clique_graph(n),
            "Line": generate_line_graph(n),
            "Ring": generate_ring_graph(n),
            "Hub": generate_hub_graph(n)}[g_type]

def generate_clique_graph(n):
    return generate(n, n * (n - 1) // 2, directed=False)

def generate_line_graph(n):
    g = graph()

    for i in range(0, n):
        g.add_node(i)
    for i in range(0, n-1):
        g.add_edge((i, i+1))

    return g

def generate_ring_graph(n):
    g = graph()

    for i in range(0, n):
        g.add_node(i)
    for i in range(0, n-1):
        g.add_edge((i, i+1))
    g.add_edge((0, n-1))

    return g

def generate_hub_graph(n):
    g = graph()

    for i in range(0, n):
        g.add_node(i)
    for i in range(1, n):
        g.add_edge((0, i))

    return g

def generate_source_graph(source):

    with open(source, 'r') as f:
        g = json.loads(f.read())

    new_graph = digraph()

    for node in g["nodes"]:
        new_graph.add_node(node)

    for edge in g["edges"]:
            new_graph.add_edge(edge=(edge["from"], edge["to"]), wt=edge["wt"])

    return new_graph
