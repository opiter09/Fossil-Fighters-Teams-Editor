import os
import shutil
import subprocess
import sys

f = open(sys.argv[1], "rb")
test = f.read()[12]
f.close()
if (test == ord("Y")):
    rom = "ff1"
else:
    rom = "ffc"

if (os.path.exists("NDS_UNPACK") == False):
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    if (rom == "ff1"):
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/battle" ])
    else:
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/battle_param" ])

if (rom == "ff1"):
    nameDiff = 3362
else:
    nameDiff = 0x4D

f = open(rom + "_enemyNames.txt", "rt")
eNames = list(f.read().split("\n"))
f.close()
for i in range(len(eNames)):
    eNames[i] = eNames[i] + " (" + str(i + nameDiff).zfill(4) + ")"

f = open(rom + "_vivoNames.txt", "rt")
vNames = list(f.read().split("\n"))
f.close()
vNames = ["NONE"] + vNames

sfTable = { "0": "NONE", "900": "Silver Head", "901": "Silver Body", "902": "Silver Arms", "903": "Silver Legs", "904": "Gold" }
teamList = []    
   
if (rom == "ff1"):
    teams = {}
    for root, dirs, files in os.walk("NDS_UNPACK/data/battle/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                if (len(r) > 0x94):
                    teamN = os.path.join(root, file).split("\\")[-2]
                    teamList.append(teamN)
                    teams[teamN] = {}
                    teams[teamN]["numVivos"] = r[0x5C]
                    numVivos = teams[teamN]["numVivos"]
                    teams[teamN]["points"] = int.from_bytes(r[0x54:0x58], "little")
                    if (teams[teamN]["points"] == 0xFFFFFFFF):
                        teams[teamN]["points"] = 0
                    teams[teamN]["name"] = eNames[int.from_bytes(r[0x64:0x66], "little") - nameDiff]
                    teams[teamN]["rank"] = r[0x68]
                    teams[teamN]["vivos"] = []
                    for i in range(numVivos):
                        teams[teamN]["vivos"][i] = {}
                        teams[teamN]["vivos"][i]["vivoNum"] = int.from_bytes(r[(0x94 + (i * 12)):(0x94 + (i * 12) + 4)], "little")
                        teams[teamN]["vivos"][i]["level"] = int.from_bytes(r[(0x94 + (i * 12) + 4):(0x94 + (i * 12) + 8)], "little")
                        teams[teamN]["vivos"][i]["superName"] = "NONE"
                        teams[teamN]["vivos"][i]["superPoints"] = 0
                        teams[teamN]["vivos"][i]["cpu"] = int.from_bytes(r[(0x94 + (numVivos * 12) + (i * 4)):(0x94 + (numVivos * 12) + (i * 4) + 4)])
                        teams[teamN]["vivos"][i]["fossils"] = int.from_bytes(r[(0x94 + (numVivos * 16) + (i * 4)):(0x94 + (numVivos * 16) + (i * 4) + 4)])
else:
    for root, dirs, files in os.walk("NDS_UNPACK/data/battle_param/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                if (len(r) > 0x46) and (r[0x34] == 0):
                    teamN = os.path.join(root, file).split("\\")[-2]
                    teamList.append(teamN)
                    teams[teamN] = {}
                    shift = r[0x38] + 2 - 0x46
                    teams[teamN]["numVivos"] = r[0x58 + shift]
                    numVivos = teams[teamN]["numVivos"]
                    teams[teamN]["points"] = int.from_bytes(r[0x30:0x32], "little")
                    if (teams[teamN]["points"] == 0xFFFFFFFF):
                        teams[teamN]["points"] = 0
                    teams[teamN]["name"] = eNames[int.from_bytes(r[(0x46 + shift):(0x48 + shift)], "little") - nameDiff]
                    teams[teamN]["rank"] = r[0x48 + shift]
                    teams[teamN]["vivos"] = []
                    for i in range(numVivos):
                        teams[teamN]["vivos"][i] = {}
                        teams[teamN]["vivos"][i]["vivoNum"] = int.from_bytes(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)], "little")
                        teams[teamN]["vivos"][i]["level"] = int.from_bytes(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)], "little")
                        teams[teamN]["vivos"][i]["superName"] = sfTable[str(int.from_bytes(r[(0x70 + shift + (i * 12) + 6):(0x70 + shift + (i * 12) + 8)], "little"))]
                        teams[teamN]["vivos"][i]["superPoints"] = int.from_bytes(r[(0x70 + shift + (i * 12) + 8):(0x70 + shift + (i * 12) + 10)], "little")
                        teams[teamN]["vivos"][i]["cpu"] = 0
                        teams[teamN]["vivos"][i]["fossils"] = int.from_bytes(r[(0x70 + shift + (numVivos * 16) + (i * 2)):(0x70 + shift + (numVivos * 16) + (i * 2) + 2)], "little")

 
# subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
# subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
# psg.popup("You can now play out.nds!", font = "-size 12")
    