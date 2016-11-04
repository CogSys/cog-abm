import pandas as pd

ts = pd.read_csv("top_shift_results_final.csv", index_col=[0, 1])
ts.index.names = ["Topology", "Iteration"]

for g in ts.index.levels[0]:
    ts.loc[g].to_csv("top_shift_{0}.csv".format(g))

ts = pd.read_csv("top_shift_ccw_final.csv", index_col=[0, 1])
ts.index.names = ["Topology", "Iteration"]

for g in ts.index.levels[0]:
    ts.loc[g].to_csv("top_shift_ccw_{0}.csv".format(g))

es = pd.read_csv("env_shift_results_final.csv", index_col=[0, 1])
es.index.names = ["Topology", "Iteration"]

for g in es.index.levels[0]:
    es.loc[g].to_csv("env_shift_{0}.csv".format(g))

es = pd.read_csv("env_shift_gauss_results_final.csv", index_col=[0, 1])
es.index.names = ["Topology", "Iteration"]

for g in es.index.levels[0]:
    es.loc[g].to_csv("env_shift_gauss_{0}.csv".format(g))

es = pd.read_csv("env_shift_gauss_ccw_final.csv", index_col=[0, 1])
es.index.names = ["Topology", "Iteration"]

for g in es.index.levels[0]:
    es.loc[g].to_csv("env_shift_gauss_ccw_{0}.csv".format(g))


with open("top_shift_mason.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{L}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            f.write("\\addlegendentry{fully connected}\n")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{G}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("top_shift_mason_ccw.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth,"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean category count]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            f.write("\\addlegendentry{fully connected}\n")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Lexicon size]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("top_shift_star.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{L}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            f.write("\\addlegendentry{fully connected}\n")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            if label == "hub":
                label = "star balanced"
            elif label == "hub hearer":
                label = "star speaker"
            elif label == "hub speaker":
                label = "star hearer"
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{G}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("top_shift_star_ccw.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth,"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean category count]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            f.write("\\addlegendentry{fully connected}\n")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            if label == "hub":
                label = "star balanced"
            elif label == "hub hearer":
                label = "star speaker"
            elif label == "hub speaker":
                label = "star hearer"
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Lexicon size]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/top_shift_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("env_shift.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{L}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            f.write("\\addlegendentry{fully connected}\n")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            if label == "hub":
                label = "star balanced"
            elif label == "hub hearer":
                label = "star speaker"
            elif label == "hub speaker":
                label = "star hearer"
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{G}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("env_shift_gauss.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{A}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            if g in ["max_avg_bet", "min_avg_bet"]:
                f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                        "y=CSA_mean] "\
                        "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            else:
                f.write("\\addplot +[draw=none] table[col sep=comma, x=Iteration, "\
                        "y=CSA_mean] "\
                        "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))


    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))

    f.write("\\legend{fully connected, max avg bet, , , , , min avg bet, , , star balanced, star speaker, star hearer}")
    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{B}]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
        if g in ["max_avg_bet", "min_avg_bet"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
        else:
            f.write("\\addplot +[draw=none] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))


    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("env_shift_gauss_ccw.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=25"\
            "xlabel=Iterations, "\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean category count]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            if g in ["max_avg_bet", "min_avg_bet"]:
                f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                        "y=cc_mean] "\
                        "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))
            else:
                f.write("\\addplot +[draw=none] table[col sep=comma, x=Iteration, "\
                        "y=cc_mean] "\
                        "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))


    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=cc_mean] "\
                    "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))

    f.write("\\legend{fully connected, max avg bet, , , , , min avg bet, , , star balanced, star speaker, star hearer}")
    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,25);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "cycle multi list={Dark2-8},"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Lexicon size]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
        if g in ["max_avg_bet", "min_avg_bet"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
        else:
            f.write("\\addplot +[draw=none] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))


    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=wc] "\
                    "{{simulation_results/env_shift_gauss_ccw_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")
