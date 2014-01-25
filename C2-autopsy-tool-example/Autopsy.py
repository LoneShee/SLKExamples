import Historyfileparser
import Chemicalsparser

Norns=Historyfileparser.Norns
Chemicals=Chemicalsparser.Chemicals

print "Dead norns:"

for Norn in  Norns:
    if Norns[Norn]["State"]=="dead":
        print Norn +"("+Norns[Norn]["Genus"]+" "+Norns[Norn]["Lifestage"]+")",
        

who = raw_input("\nEnter a moniker: ").upper()
NornChems=Norns[who]["ChemicalsAtDeath"]

print "Diagnosing death of "+Norns[who]["Name"] + "("+Norns[who]["Moniker"]+"):" # He's not a moniker! In death, members of project CAOS do have a name
print "Subject data: " + Norns[who]["Gender"] +" " + Norns[who]["Genus"] + "\t Dead as:" + Norns[who]["Lifestage"]
print "-"*50

if Norns[who]["Lifestage"]=="Kaputt":
    print "Creature most likely died of old age"

for num, chem in enumerate(NornChems):
    if Chemicals[num] !="" and Chemicals[num] !=" ":
        print (Chemicals[num] +":"+str(ord(chem))+"\t").expandtabs(20),
        if num % 5 ==0:
            print ""
