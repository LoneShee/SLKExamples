import os
import struct

def readbyte( readfromfile ):
    return struct.unpack("B",readfromfile.read(1))[0]

def readLong( readfromfile ):
    return struct.unpack("L",readfromfile.read(struct.calcsize("L")))[0]

def readCstring (readfromfile):
    """
    CStrings are strings which have length data linked with them. The format
    is flexible and they are read as follows:

    READ BYTE Length
    If Length=255 then READ WORD Length
    READ Char[Length] into String
    """
    strlength = struct.unpack("B", readfromfile.read(1))[0]
    if strlength == 0xff:
        strlength = struct.unpack("H", readfromfile.read(2))[0]
    return readfromfile.read(strlength)

#Change this accordingly :
GamePath="C:\Creatures2\History"

os.chdir(GamePath)
files=os.listdir(".")

Norns={}
for histfile in files:
    if histfile[0:2]=="cr":
        Norns[histfile[3:]]={}
        fic=open(histfile,"rb")

        Moniker=fic.read(4)
       	Norns[Moniker]["Moniker"]=Moniker 

        Name=readCstring(fic)
        Norns[Moniker]["Name"]=Name

        MumMoniker=fic.read(4)
        Norns[Moniker]["MumMoniker"]=MumMoniker

        MomName=readCstring(fic)
        Norns[Moniker]["MomName"]=MomName

        DadMoniker=fic.read(4)
        if DadMoniker !="\x00\x00\x00\x00":
            Norns[Moniker]["DadMoniker"]=str(DadMoniker)
        else:
            Norns[Moniker]["DadMoniker"]=""
            
        DadName=readCstring(fic)
        Norns[Moniker]["DadName"]=DadName

        BirthDate=readCstring(fic)
        Norns[Moniker]["BirthDate"]=BirthDate

        BirthPlace=readCstring(fic)
        Norns[Moniker]["BirthPlace"]=BirthPlace

        OwnerName=readCstring(fic)
        Norns[Moniker]["OwnerName"]=OwnerName

        OwnerURL=readCstring(fic)
        Norns[Moniker]["OwnerURL"]=OwnerURL
        
        OwnerNotes=readCstring(fic)
        Norns[Moniker]["OwnerNotes"]=OwnerNotes

        OwnerMail=readCstring(fic)
        Norns[Moniker]["OwnerMail"]=OwnerMail

        State=readLong(fic)
        State=["alive","dead","exported"][State] #Isn't python awesome ?
        Norns[Moniker]["State"]=State

        Gender=readLong(fic)
        Gender=[None,"male","female"][Gender] 
        Norns[Moniker]["Gender"]=Gender

        Age=readLong(fic)
        Norns[Moniker]["Age"]=Age

        Epitaph=readCstring(fic)
        Norns[Moniker]["Epitaph"]=Epitaph

        GravePhotoIndex=readLong(fic)
        Norns[Moniker]["GravePhotoIndex"]=GravePhotoIndex

        TimeOfDeath=readLong(fic)
        Norns[Moniker]["TimeOfDeath"]=TimeOfDeath

        TimeOfBirth=readLong(fic)
        Norns[Moniker]["TimeOfBirth"]=TimeOfBirth

        TimeOfAdolescence=readLong(fic) # Yay! Kisspoping time !
        Norns[Moniker]["TimeOfAdolescence"]=TimeOfAdolescence

        DeathRegistered=readLong(fic)
        DeathRegistered=["no","yes"][DeathRegistered] 
        Norns[Moniker]["DeathRegistered"]=DeathRegistered

        Genus=readLong(fic)
        Genus=[None,"Norn","Grendel","Ettin"][Genus] 
        Norns[Moniker]["Genus"]=Genus

        Lifestage=readLong(fic)
        Lifestage=["Baby","Child","Adolescent","Youth","Adult","Old","Senile","Kaputt"][Lifestage] 
        Norns[Moniker]["Lifestage"]=Lifestage

        ChemicalsAtDeath=fic.read(256)
        Norns[Moniker]["ChemicalsAtDeath"]=ChemicalsAtDeath

