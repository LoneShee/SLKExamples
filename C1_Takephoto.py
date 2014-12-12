# -*- coding: cp1252 -*-
import win32ui
import dde
import struct
import Image



C1Path="c:/Creatures/"
Outfile="Out.spr"

#dde: pict   parameters :
P1=0xff # Width
P2=0x10 # Unknown
P3=0xff # Height

def readLong( readfromfile ):
    return struct.unpack("L",readfromfile.read(struct.calcsize("L")))[0]

def readWord( readfromfile ):
    return struct.unpack("H",readfromfile.read(struct.calcsize("H")))[0]

def readSpriteHeader(readfromfile):
    header={}
    header["Offset"]=readLong(readfromfile)
    header["Width"]=readWord(readfromfile)
    header["Height"]=readWord(readfromfile)
    return header

def SendCommandToGame(command,ExpectedResult=False):
    """
    This function sends a CAOS command to a C1 or C2 game and returns the result
    You have to specify whether or not the executed command expects output to be returned, as both kinds of commands require different calls
    """
    server = dde.CreateServer()
    server.Create("TestClient")
    conversation = dde.CreateConversation(server)

    conversation.ConnectTo("Vivarium", "Anything")
    conversation.Poke("Macro", command+"\x00")

    if ExpectedResult==True:
        rep=conversation.Request("Macro")
    else:
        conversation.Exec(command+"\x00")
        rep=""
    server.Destroy()
    
    return rep

def MakeSprFile(Width,Height,Data,outfile):
    fic=open(outfile,"wb")
    fic.write(struct.pack("H",1))
    fic.write(struct.pack("L",10))
    fic.write(struct.pack("H",Width))
    fic.write(struct.pack("H",Height))
    print len(Data)
    fic.write(Data)
    

rep =SendCommandToGame("inst,dde: panc,dde: pict "+chr(P1)+chr(P2)+chr(P3)+",endm",True)
print rep

fic=open(C1Path+rep,"rb")
fic.seek(0, 2)
filesize=fic.tell()
fic.seek(0)
print "Filesize : %d" % filesize

one=readLong(fic)
two=readLong(fic)
three=readLong(fic)

data=fic.read(fic.tell()-filesize)
print str(one),str(two),str(three),len(data)

MakeSprFile(one,two,data,C1Path+Outfile)


# Open our sprite file
fic=open(C1Path+Outfile,"rb")

#Read the palette file as a list of bytes.
palette=[ord(byte) for byte in list(open(C1Path+"/Palettes/Palette.dta","rb").read())]

TheFile={}

# Read the first 32 bits corresponding to number of images to expect
TheFile["nbImg"]=readWord(fic)
print "The file contains %d images" % (TheFile["nbImg"])

#Read out as many image headers as there are files
for i in range(1,TheFile["nbImg"]+1):
    TheFile[i]=readSpriteHeader(fic)
    print "Image N° %d starts at %d and is %d x %d" % (i,TheFile[i]["Offset"],TheFile[i]["Width"],TheFile[i]["Height"])

# For each of the expected umages:
for i in range(1,TheFile["nbImg"]+1):
    #Read the image data
    TheFile[i]["data"]=fic.read(TheFile[i]["Width"]*TheFile[i]["Height"])
    #Create PIL image from the data
    im=Image.fromstring("P", (TheFile[i]["Width"], TheFile[i]["Height"]),TheFile[i]["data"], "raw","P")
    # Apply the game palette ( Remember that according to doc, all bytes of the palette should be multiplied by 4 before usage
    # Not doing so will result in dark images
    im.putpalette([color * 4 for color in palette])
    # Show image, right side up
    im.transpose(Image.FLIP_TOP_BOTTOM).show()

