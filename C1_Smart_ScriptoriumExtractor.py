import win32ui
import dde
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    
outpath=application_path+"/Scriptorium extract/"
print outpath

def SendCommandToGame(command,ExpectedResult=False):
    """
    This function sends a CAOS command to a C1 or C2 game and returns the result
    You have to specify whether or not the executed command expects output to be returned, as both kinds of commands require different calls
    """
    server = dde.CreateServer()
    server.Create("TestClient") # This can be anything or even empty.
    conversation = dde.CreateConversation(server)

    conversation.ConnectTo("Vivarium", "Anything")
    conversation.Poke("Macro", command+"\x00") # Rembember Creature expects C-style \0 terminated strings as DDE inputs
    if ExpectedResult==True:
        # If the command returns a result use the Request() method
        rep=conversation.Request("Macro")
    else:
        # If the command doesn't a result use the exec() method
        conversation.Exec(command+"\x00")
        rep=""

    server.Destroy()
    return rep


def GetAllScripts(classifier):

    if not os.path.exists(outpath):
        os.makedirs(outpath)
        
    Scripts={}
    for i in range (0,255):
        res=SendCommandToGame("dde: scrp "+ classifier + " " + str(i),True)
        if res.strip() not in  (""," ","\n","\r\n",None):
            Scripts[classifier+" "+ str(i)]=res
            DumpScript(classifier+" "+ str(i),res)
            print "X",
        else:
            print ".",
    return Scripts

def DumpScript(Classifier,Contents):
    f=open(outpath+Classifier+".txt","w")
    f.write(Contents)
    f.close()
    

#######
#Level3={'2 8 15': 1, '2 3 8': 1, '2 3 9': 1, '3 1 11': 1, '2 10 6': 1, '2 3 4': 24, '2 3 5': 3, '2 3 6': 1, '2 3 7': 1, '3 3 1': 1, '2 3 1': 1, '2 3 2': 1, '2 3 3': 4, '3 1 9': 1, '2 10 4': 3, '3 1 3': 1, '2 4 9': 1, '2 5 6': 1, '2 10 2': 4, '2 15 4': 1, '4 2 1': 1, '3 1 1': 4, '2 14 3': 1, '3 1 10': 1, '2 3 10': 1, '2 4 13': 1, '2 4 11': 1, '2 4 10': 1, '2 13 1': 1, '4 1 1': 2, '4 1 2': 1, '2 11 1': 1, '2 15 5': 1, '2 10 7': 3, '2 9 6': 1, '2 10 5': 3, '3 4 1': 1, '2 10 3': 4, '2 14 1': 1, '2 10 1': 4, '2 12 2': 2, '2 15 6': 1, '2 9 4': 1, '2 10 9': 1, '2 3 100': 1, '2 15 2': 1, '2 9 5': 1, '3 1 12': 1, '2 13 2': 3, '3 1 6': 1, '2 12 1': 1, '3 5 1': 1, '2 13 3': 1, '2 9 3': 1, '2 6 1': 22, '2 14 2': 1, '2 6 3': 11, '2 6 2': 7, '2 9 2': 1, '2 6 4': 5, '2 9 1': 1, '2 7 1': 1, '2 7 2': 6, '2 15 7': 1, '2 8 100': 1, '3 2 1': 9, '2 8 9': 2, '2 8 8': 1, '2 8 7': 1, '2 15 3': 1, '2 15 1': 1, '2 8 3': 1, '2 8 2': 1, '2 8 1': 3, '2 1 1': 1}
#for entity in Level3.keys():
#    print "\nretriving scripts for %s:" % (entity)
#    GetAllScripts(entity)
#######


ScriptoriumNumbers={}

# Pause the game so agent quantities remain stable :
print SendCommandToGame("sys: cmnd 32838",False)

# Scanning firt row:
print "="*15,"Scanning Families","="*15
for family in range(1,255):
    print ".",
    Number = int(SendCommandToGame("dde: putv totl "+ str(family) +" 0 0",True))
    if Number > 0:
        print "[%s :%s]" % (family,Number),
        ScriptoriumNumbers[family]=Number
        
        
print "Finished first level"

print ScriptoriumNumbers


Level2={}
print "="*15,"Scanning Genuses","="*15
for family in ScriptoriumNumbers :
    found =0
    print "Scanning the %s branch" % str(family)
    for genus in range(1,255):
        print ".",
        Number = int(SendCommandToGame("dde: putv totl "+ str(family) +" "+str(genus)+" 0",True))
        if Number > 0:
            print "[%s %s :%s]" % (family,genus,Number),
            Level2[str(str(family)+" "+str(genus))]=Number
            found= found + Number
            if found==int(ScriptoriumNumbers[family]):
                print "\nFound expected qty of members,skipping rest of Family"
                break
        
print Level2





Level3={}
print "="*15,"Scanning Species","="*15
for FamilyGenus in Level2:
    found=0
    for species in range(1,255):
        #print "trying" + str(FamilyGenus)+" "+ str(species)
        print ".",
        Number = int(SendCommandToGame("dde: putv totl "+str(FamilyGenus)+" "+ str(species),True))
        if Number > 0:
            print "[%s %s:%s]" % (FamilyGenus,species,Number),
            Level3[str(str(FamilyGenus)+" "+str(species))]=Number
            found= found + Number
            if found==int(Level2[FamilyGenus]):
                print "\nFound expected qty of members,skipping rest of specie"
                break

print ScriptoriumNumbers
print Level2
print Level3


print "="*15,"Retriving All scripts for found entities","="*15
print "="*15,"Relax and sit back, this will take a while (~1hr expected)","="*15
for entity in Level3.keys():
    print "retriving scripts for %s:" % (entity)
    GetAllScripts(entity)
