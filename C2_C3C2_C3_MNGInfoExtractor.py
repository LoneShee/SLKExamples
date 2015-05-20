import struct
import mmap
import wave
import re
import sys
import os



def readLong( readfromfile ):
    return struct.unpack("L",readfromfile.read(struct.calcsize("L")))[0]

def readWord( readfromfile ):
    return struct.unpack("H",readfromfile.read(struct.calcsize("H")))[0]

def decryptScript(contents):
    cleartext=[]
    key=0x05
    for index,byte in enumerate(contents):
        cleartext.append(   chr(ord(byte) ^ key)        )
        key=(key + 0xc1 )%256
    return ''.join(cleartext)
    
def dumpWaveFile(where,sampledata):
    wav=wave.open(where,'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(22000)
    wav.setcomptype("NONE","not compressed")
    wav.writeframesraw(sampledata)
    wav.close()
    
def uniqueItems(seq):
    #seq =[item[0] for item in seq]
    #print seq
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def findWaveNames(where):
    items=re.findall('[^a-zA-Z0-9]Wave\((.*)\)',where, re.IGNORECASE)
    items =[item.split(')')[0] for item in items ] # some Wave() mentions are followed by other functions on the same line
    items=uniqueItems(items)
    #print len(items)
    #print items
    return items

def findTrackNames(where):
    items=re.findall('[^a-zA-Z0-9]Track\((.*)\)',where, re.IGNORECASE)
    items=uniqueItems(items)
    return items

if len(sys.argv)<2:
    raw_input("Please drag and drop a .mng file on this executable...")
    sys.exit(1)

musicFile=sys.argv[1].replace('\\','/')

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

sys.stdout = open(application_path+ '/Infos.txt', 'w')

outpath=application_path+"/out_"+musicFile.split("/")[-1]+"/"

if not os.path.exists(outpath):
    os.makedirs(outpath)

theFile={}

with open(musicFile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    theFile["numSamples"]=int(readLong(f))
    print "The file %s contains %s samples" % (musicFile,theFile["numSamples"])
    
    theFile["scriptStart"]=readLong(f)
    #print "The script starts at %s" % theFile["scriptStart"]

    theFile["scriptLen"]=readLong(f)
    #print "The script is %s bytes long" % theFile["scriptLen"] 

    theFile["mangledScript"]=mm[theFile["scriptStart"]:theFile["scriptStart"]+theFile["scriptLen"]]
    theFile["script"]=decryptScript(theFile["mangledScript"])
    segment=theFile["script"][100:300]
    #print "... %s ..." % theFile["script"][100:300]

    theFile["wavenames"]=findWaveNames(theFile["script"])
    
    print "="*64+"\nThe wave names are : %s " % theFile["wavenames"]
    
    theFile["samples"]={}
    for i in range(1,theFile["numSamples"]+1):
        theFile["samples"][i]={}
        theFile["samples"][i]["start"]=readLong(f)
        theFile["samples"][i]["length"]=readLong(f)
        #print "sample %s starts at %s and is %s bytes long" % (i,theFile["samples"][i]["start"],theFile["samples"][i]["length"])
        theFile["samples"][i]["data"]=mm[theFile["samples"][i]["start"]:theFile["samples"][i]["start"]+theFile["samples"][i]["length"]]
        dumpWaveFile(outpath+theFile["wavenames"][i-1]+".wav",theFile["samples"][i]["data"])

    theFile["trackNames"]=findTrackNames(theFile["script"])
    print "="*64+"\nThere are %s tracks : %s" % (len(theFile["trackNames"]),theFile["trackNames"])

script=open(application_path+"/"+musicFile.split("/")[-1]+"_Script.txt","w")
script.write(theFile["script"])
script.close()
