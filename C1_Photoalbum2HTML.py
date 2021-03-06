import os
import struct
import Image

GamePath="C:/Creatures/"
SaveDir=GamePath+"HTMLGallery/"
ResDir=SaveDir+"img/"
galleryfile=SaveDir+"Gallery.html"

def readLong( readfromfile ):
    return struct.unpack("L",readfromfile.read(struct.calcsize("L")))[0]

def readWord( readfromfile ):
    return struct.unpack("H",readfromfile.read(struct.calcsize("H")))[0]

def readCstring (readfromfile):
    """
    Acording to the CDN, CStrings are strings which have length data linked with them.
    Their format is flexible depending on string length and they are read as follows:

    READ BYTE Length
    If Length=255 then READ WORD Length
    READ Char[Length] into String
    
    CStrings are often used inside the various game files.
    """
    #print "reading Cstring"
    byte=readfromfile.read(1)
    if byte=="" :
        return None
    strlength = struct.unpack("B", byte)[0]
    if strlength==0x00:
        byte=readfromfile.read(1)
        return None
    
    if strlength == 0xff:   # if the length byte is 255, we need to read next word instead.
        strlength = struct.unpack("H", readfromfile.read(2))[0]
    return readfromfile.read(strlength)


Picfiles=[f for f in os.listdir(GamePath) if f[-11:]=="Photo Album"]

print Picfiles

if not os.path.isdir(SaveDir):
    os.makedirs(SaveDir)

if not os.path.isdir(ResDir):
    os.makedirs(ResDir)

#Read the palette file as a list of bytes.
palette=[ord(byte) for byte in list(open(GamePath+"/Palettes/Palette.dta","rb").read())]

def MkFileFromData(Entry,palette):
    im=Image.fromstring("P", (Entry["Width"], Entry["Height"]),Entry["Data"], "raw","P")
    im.putpalette([color * 4 for color in palette])
    outfile=ResDir+Entry["SrcFile"][:8]+"_"+str(Entry["Num"])+".bmp"
    im.transpose(Image.FLIP_TOP_BOTTOM).save(outfile)
    return outfile

def ProcessFile(PhotoAlbum):
    TheFile={}
    TheFile["Entries"]=[]
    fullpath=GamePath+PhotoAlbum
    fic=open(fullpath,"rb")
    TheFile["NumEntries"]=readWord(fic)
    TheFile["Moniker"]=PhotoAlbum[:7]
    #print "File has %s entries" % TheFile["NumEntries"]
    remaining=TheFile["NumEntries"]
    while remaining !=0:
        TheEntry={}
        
        TheEntry["Num"]=TheFile["NumEntries"]-remaining       
        TheEntry["SrcFile"]=PhotoAlbum
        TheEntry["Timestamp"]=readCstring(fic)
        TheEntry["Width"]=readLong(fic)
        TheEntry["Height"]=readLong(fic)
        TheEntry["Unused"]=readLong(fic)
        TheEntry["Data"]=fic.read(TheEntry["Height"]*TheEntry["Width"])
        # Jump back 2 bytes because of nown size bug in the files
        fic.seek(fic.tell()-2)
        TheEntry["Comment"]=readCstring(fic)
        TheEntry["Image"]=MkFileFromData(TheEntry,palette)

        TheFile["Entries"].append(TheEntry)
        remaining=remaining-1

    return TheFile

Gallery=[]

for f in Picfiles:
    Gallery.append(ProcessFile(f))

outtext="<html><body>"
for elem in Gallery:
    outtext=outtext+"<hr>"
    outtext=outtext+"Gallery for: "+elem["Moniker"] +"<br>"
    for entry in elem["Entries"]:
      outtext=outtext+"<img src='file://" +entry["Image"]+"'>"+entry["Timestamp"]+"-"+str(entry["Comment"])  
outtext=outtext+"</html></body>"

open(galleryfile,"w").write(outtext)
