import struct

number=0
Chemicals={}

f = open("Chemicals.txt", "rb")
try:
    byte = struct.unpack("H",f.read(2))[0]
    while byte != "\x00\x00":

         # We are reading a chemical entry

         if number < 256:
            Chemname = f.read(byte)
            Chemicals[number] = {"number":number,"name":Chemname}
            #print Chemicals[number]["number"],":",Chemicals[number]["name"]
            number+=1
            byte = struct.unpack("H",f.read(2))[0]

         # We are skipping the \x00\x00\x00\x00 marker

         elif number == 256:
            byte = struct.unpack("H",f.read(2))[0]
            number+=1

         # We are reading a chem description entry

         elif number < 513:
                Chemdesc=f.read(byte)
                Chemicals[number-257]["desc"]=Chemdesc
                number+=1
                byte = struct.unpack("H",f.read(2))[0]
        else:
                break
finally:
    f.close()

# printout chemicals recovered :
for chemical in Chemicals:
    print Chemicals[chemical]["number"],":",Chemicals[chemical]["name"],"(",Chemicals[chemical]["desc"],")"
