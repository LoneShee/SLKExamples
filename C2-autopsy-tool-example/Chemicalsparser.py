import os
import struct

def readword( readfromfile ):
    return struct.unpack("H",readfromfile.read(2))[0]

def readCstring (readfromfile):
    """
    CStrings are strings which have length data linked with them. The format
    is flexible and they are read as follows:

    READ BYTE Length
    If Length=255 then READ WORD Length
    READ Char[Length] into String
    """
    byte=readfromfile.read(1)
    if byte=="":
        return None
    strlength = struct.unpack("B", byte)[0]
    if strlength == 0xff:
        strlength = struct.unpack("H", readfromfile.read(2))[0]
    return readfromfile.read(strlength)

chemfile=open("../allchemicals.str","rb")
#chemfile=open("allchemicalsFR.str","rb")
#chemfile=open("allchemicalsDE.str","rb")

Chemicals=[]

Header=readword(chemfile)
entry=readCstring(chemfile)

while entry != None:
        Chemicals.append(entry)
        entry=readCstring(chemfile)

