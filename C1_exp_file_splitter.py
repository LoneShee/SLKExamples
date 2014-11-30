"""
This script splits a C1 .exp file into its 5 main sections to ease reverse
engineering of the format.
"""

import re

with  open("C1_Norn.exp","rb") as fic:
    contents=fic.read()
    print "File is %d bytes long " % len(contents)
    Sections=re.finditer(b"C[A-Z][a-z]+",contents)
    Offsets=[section.start() for section in Sections]
    Offsets.insert(0,0)
    Offsets.append(len(contents))
##    for offset in Offsets:
##        print format(offset,'02x')
    
    Sections=[]
    for num,offset in enumerate(Offsets):
        if num >0:
            Sections.append((Offsets[num-1],Offsets[num]-1))
            print "Range : %s-%s (%s-%s)" %(Offsets[num-1],Offsets[num]-1,format(Offsets[num-1],'02x'),format(Offsets[num]-1,'02x'))


    for num,section in enumerate(Sections):
        if section[0] !=0:
            fic.seek(section[0]-2)
            data=fic.read(section[1]-section[0]+1)
        else:
            fic.seek(section[0])
            data=fic.read(section[1]-section[0]-1)
        fo = open("C1_Norn.exp_"+"Section_"+str(num), "wb")
        fo.write(data)
        fo.close()


