import pydot
import Historyfileparser

tree = pydot.Dot(graph_type='digraph') # Digraph means "oriented links"

#print Historyfileparser.Norns["1KTQ"]

for moniker in Historyfileparser.Norns.keys():
    print moniker,":", Historyfileparser.Norns[moniker]["DadMoniker"],Historyfileparser.Norns[moniker]["MumMoniker"]
    tree.add_edge(pydot.Edge(Historyfileparser.Norns[moniker]["MumMoniker"], moniker))

    if Historyfileparser.Norns[moniker]["DadMoniker"]!="":
        tree.add_edge(pydot.Edge(Historyfileparser.Norns[moniker]["DadMoniker"], moniker))

tree.write_png('./Familytree.png')
