def parse_to_json_graph(file_name):
    f = open(file_name, 'r')

    nodes = f.readline().split()
    nodes = [ int(node) for node in nodes]
    edges = []
    for line in f:
        edge = line.split()
        if len(edge) > 0:
            edges.append({"to": int(edge[0]), "from": int(edge[1]), "wt": 1})

    f.close()
    f = open(file_name + '.json', 'w')

    import json

    json.dump({"nodes": nodes, "edges": edges}, f)
    f.close()

if __name__ == "__main__":
    import optparse
    opt_p = optparse.OptionParser()
    opt_p.add_option('-f', '--file', action="store", dest='file', type="string",
                     help="output file with results")
    opts, args = opt_p.parse_args()
    parse_to_json_graph(opts.file)
