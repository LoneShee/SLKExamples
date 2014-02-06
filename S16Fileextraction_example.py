import struct
import Image

def readbyte( readfromfile ):
    return struct.unpack("B",readfromfile.read(1))[0]

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

fic=open("Photo_0BLT.s16","rb")

TheFile={}

flags=readLong(fic)
TheFile["Flags"]=flags
print "The file is in " + ["555","565"][flags] +" format."

SpriteCount=readWord(fic)
TheFile["SpriteCount"]=SpriteCount
print "The file has %d sprites" % SpriteCount

for i in range(1,TheFile["SpriteCount"]+1):
    TheFile[i]=readSpriteHeader(fic)
    print "Image N° %d starts at %d and is %d x %d" % (i,TheFile[i]["Offset"],TheFile[i]["Width"],TheFile[i]["Height"])
    
print TheFile 

#For each sprite:
for i in range(1,TheFile["SpriteCount"]+1):
    #Read the corresponding data:
    TheFile[i]["data"]=fic.read(TheFile[i]["Width"]*TheFile[i]["Height"]*2)

    #BGR;16 is the 565 format,  BGR;15 is for 555
    if flags==1:
        im=Image.fromstring("RGB", (TheFile[i]["Width"], TheFile[i]["Height"]),TheFile[i]["data"], "raw", "BGR;16")
    else:
        im=Image.fromstring("RGB", (TheFile[i]["Width"], TheFile[i]["Height"]),TheFile[i]["data"], "raw", "BGR;15")

    im.show()


