"""
This POC shows how to parse a C1 sprite file data and extract corresponding images
"""

import struct
import Image

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

# Open a sample file
fic=open("raio.SPR","rb")

#Read the palette file as a list of bytes.
palette=[ord(byte) for byte in list(open("Palette.dta","rb").read())]

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
    # Output each sprite to a readable format.
    im.save("Image_"+str(i)+".png")
