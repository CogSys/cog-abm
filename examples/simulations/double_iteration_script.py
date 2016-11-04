# this script helps to provide specific simulation file. The second iteration was added to measure CS and DS, where all agents meet together, but they still learn in fixed network. Content of the new file should be added to simulation file
interactions = ""

for i in range(5000):
    # interactions=""
    s = """
        {
        "type": "Clique", "start": %s
        },
        """ % (10000 + 2 * i + 1)
    s2 = """
        {
        "type": "Line", "start": %s
        },
        """ % (10000 + 2 * i + 2)
    interactions = interactions + s + s2
f = open('iterations.txt', 'w')
f.write(interactions)
f