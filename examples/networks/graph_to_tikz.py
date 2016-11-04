# coding: utf-8
import json
import argparse


def parse_graph(json_file, out_file):

    with open(json_file, "r") as f:
        graph = json.load(f)

    visited = set()

    with open(out_file, "w") as f:
        f.write("\\documentclass{standalone}\n"\
                "\\usepackage{tikz}\n"\
                "\\usetikzlibrary{graphs}\n"\
                "\\usetikzlibrary{graphdrawing}\n"\
                "\\usegdlibrary{force}\n"\
                "\\begin{document}\n"\
                "\\tiny\n"\
                "\\begin{tikzpicture}\n")
        f.write("\\tikzset{VertexStyle/.style = {shape=circle,\n"\
                "ball color=orange!80,\n"\
                "text=black,\n"\
                "inner sep=2pt,\n"\
                "outer sep=0pt,\n"\
                "minimum size=16 pt}}")
        f.write("\\graph [spring electrical layout',"
                "nodes={VertexStyle},"
                "node distance=6em] {\n")
        for e in graph["edges"]:
            if (e["to"], e["from"]) not in visited:
                f.write("{0} -- {1};\n".format(e["from"], e["to"]))
                visited.add((e["from"], e["to"]))
        f.write("};\n")
        f.write("\\end{tikzpicture}\n"\
                "\\end{document}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", help="JSON graph file")
    parser.add_argument("out_file", help="File to save resulting TikZ code")
    args = parser.parse_args()

    parse_graph(args.graph, args.out_file)
