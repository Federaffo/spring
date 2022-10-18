# %%
from penman.graph import Graph as GraphPen
from penman.codec import _decode, _encode
from graphtheory.structures.graphs import Graph, Edge
from graphtheory.connectivity.connected import SimpleDFS
import random

import sys
random.seed(42)


TRAIN_PATH = "train.txt"
DEV_PATH = "dev.txt"
TEST_PATH = "test.txt"

MAX_DEPTH = 2


def printInto(fileName, sid, sentence, gp):
    with open(fileName, 'a') as o:
        graph = _encode(gp)
        o.write("# ::id " + str(sid) + "\n")
        o.write(sentence)
        o.write(graph)
        o.write("\n\n")
        o.close()


def cut(s, snt, sid, max_depth):
    gp = _decode(s)

    n = len(gp.instances())
    g = Graph(n, directed=True)

    for a, _, b in gp.edges():
        g.add_edge(edge=Edge(a, b))

    # DFS on
    dfs = SimpleDFS(g)
    nodes_remove = []

    # Find node to remove from graph
    def appendorder(node, depth):
        if depth >= int(max_depth):
            nodes_remove.append(node)

    dfs.run(source=None, pre_action=appendorder)

    instances = [i for i in gp.instances() if i[0] not in nodes_remove]
    edges = [e for e in gp.edges() if e[0] not in nodes_remove and e[2]
             not in nodes_remove]

    att = [a for a in gp.attributes() if a[0] not in nodes_remove]

    triples = [*instances, *edges, *att]

    # Create a new graph
    gp = GraphPen(triples)

    # Print the cutted AMR
    if (random.random() < 0.66):
        printInto(TRAIN_PATH, sid, snt, gp)

    elif (random.random() < 0.5):
        printInto(DEV_PATH, sid, snt, gp)

    else:
        printInto(TEST_PATH, sid, snt, gp)


f = open("amr.txt", "r")
string = ""
sentence = ""
sid = 0
totalError = 0
for line in f:
    #   print(x)
    if "::snt" in line:
        sentence = line
    if (line != "\n"):
        string = string+line
    else:
        try:
            cut(string, sentence, sid, MAX_DEPTH)
        except:
            totalError += 1
            print("err")

        string = ""
        sentence = ""
        sid += 1

print(totalError)


# %%
