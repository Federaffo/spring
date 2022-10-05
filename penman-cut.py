# %%
from penman.graph import Graph as GraphPen
from penman.codec import _decode, _encode
from graphtheory.structures.graphs import Graph, Edge
from graphtheory.connectivity.connected import SimpleDFS
import random

import sys
c = 0
random.seed(42)


def cut(s, snt, mydepth):

    gp = _decode(s)

    n = len(gp.instances())
    g = Graph(n, directed=True)

    for a, _, b in gp.edges():
        g.add_edge(edge=Edge(a, b))

    dfs = SimpleDFS(g)
    nodes_remove = []

    def appendorder(node, depth):
        if depth >= int(mydepth):
            nodes_remove.append(node)

    dfs.run(source=None, pre_action=appendorder)

    instances = [i for i in gp.instances() if i[0] not in nodes_remove]
    edges = [e for e in gp.edges() if e[0] not in nodes_remove and e[2]
             not in nodes_remove]
    # print(len(edges))
    #[print(e) for e in edges]
    triples = [*instances, *edges]
    gp = GraphPen(triples)
    # print(_encode(gp))
    if(random.random() < 0.66):
        o = open("train.txt", "a")
        o.write(snt)
        o.write(_encode(gp))
        o.write("\n\n")
        o.close()
    elif(random.random() < 0.5):
        o = open("dev.txt", "a")
        o.write(snt)
        o.write(_encode(gp))
        o.write("\n\n")
        o.close()
    else:
        o = open("test.txt", "a")
        o.write(snt)
        o.write(_encode(gp))
        o.write("\n\n")
        o.close()


f = open("amr.txt", "r")
s = ""
snt = ""
err = 0
for x in f:
    #   print(x)
    if "::snt" in x:
        snt = x
    if(x != "\n"):
        s = s+x
    else:
        try:
            cut(s, snt, 3)
        except:
            print("err")
            err += 1
        s = ""
        snt = ""

print(err)

# %%
