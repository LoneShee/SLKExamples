import pydot
import Historyfileparser
import datetime
import os

imgp=os.path.realpath('./').replace("\\","/")

def makelabel(Norn):
    Name=Norn["Name"]
    if "<" in Name or ">" in Name:
        Name="Unnamed"
    
    Mnk=Norn["Moniker"]
    ToB=str(datetime.datetime.fromtimestamp(Norn["TimeOfBirth"]))

    if Norn["TimeOfDeath"] == 0:
        ToD="still alive"
    else:
        ToD="Dead: " + str(datetime.datetime.fromtimestamp(Norn["TimeOfDeath"]))

    Pictures=os.listdir("./Images/")
    
    if Norn["Moniker"]+".jpg" in Pictures:
        Pic=imgp+"/Images/"+Norn["Moniker"]+".jpg"
    else:
        Pic=imgp+"/Images/none.jpg"

    if Norn["Genus"] == "Norn" :
        spec="tan"
    elif Norn["Genus"] == "Grendel":
        spec="greenyellow"
    else:
        spec="lightyellow"
        

    label="<<table color='black'><tr><td>"+Name+" ("+Mnk+")</td></tr><tr><td><img src='"+Pic+"'/></td></tr><tr><td bgcolor='"+spec+"'>Born: "+ToB+"</td></tr><tr><td bgcolor='"+spec+"'>"+ToD+"</td></tr></table>>"

    return label

def makeborder(Norn):
    if Norn["State"]== "alive":
        bgcolor = "green"
    elif Norn["State"]== "dead":
        bgcolor = "red"
    else:
        bgcolor = "yellow"

    return bgcolor


tree = pydot.Dot(graph_type='digraph') # Digraph means "oriented links"
Nodes=[]

for moniker in Historyfileparser.Norns.keys():
    
    print moniker,":", Historyfileparser.Norns[moniker]["DadMoniker"],Historyfileparser.Norns[moniker]["MumMoniker"]
    lab=makelabel(Historyfileparser.Norns[moniker])
    clr=makeborder(Historyfileparser.Norns[moniker])
    
    if Historyfileparser.Norns[moniker]["Gender"]=="male":
        Nodes.append(pydot.Node(moniker,color=clr,shape="box",fontcolor="black",penwidth=5,label=lab,style="filled", fillcolor="lightblue"))
    else:
        Nodes.append(pydot.Node(moniker,color=clr,shape="box",fontcolor="black",penwidth=5,label=lab,style="filled", fillcolor="pink"))

    tree.add_edge(pydot.Edge(Historyfileparser.Norns[moniker]["MumMoniker"], moniker))
    if Historyfileparser.Norns[moniker]["DadMoniker"]!="":
            tree.add_edge(pydot.Edge(Historyfileparser.Norns[moniker]["DadMoniker"], moniker))

for node in Nodes:
    tree.add_node(node)


tree.write_png('./Familytree.png')
