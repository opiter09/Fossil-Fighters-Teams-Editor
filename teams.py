import os
import PySimpleGUI as psg
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
sfList = list(sfTable.values()).copy()
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
                    # print(teamN)
                    teams[teamN] = {}
                    teams[teamN]["numVivos"] = r[0x5C]
                    numVivos = teams[teamN]["numVivos"]
                    teams[teamN]["points"] = int.from_bytes(r[0x54:0x58], "little")
                    if (teams[teamN]["points"] == 0xFFFFFFFF):
                        teams[teamN]["points"] = 0
                    try:
                        teams[teamN]["name"] = eNames[int.from_bytes(r[0x64:0x66], "little") - nameDiff]
                    except IndexError:
                        teams.pop(teamN)
                        continue
                    teams[teamN]["rank"] = r[0x68]
                    teams[teamN]["vivos"] = [ {}, {}, {} ]
                    for i in range(numVivos):
                        teams[teamN]["vivos"][i]["vivoNum"] = int.from_bytes(r[(0x94 + (i * 12)):(0x94 + (i * 12) + 4)], "little")
                        teams[teamN]["vivos"][i]["level"] = int.from_bytes(r[(0x94 + (i * 12) + 4):(0x94 + (i * 12) + 8)], "little")
                        teams[teamN]["vivos"][i]["superName"] = "NONE"
                        teams[teamN]["vivos"][i]["superPoints"] = 0
                        teams[teamN]["vivos"][i]["cpu"] = int.from_bytes(r[(0x94 + (numVivos * 12) + (i * 4)):(0x94 + (numVivos * 12) + (i * 4) + 4)], "little")
                        teams[teamN]["vivos"][i]["fossils"] = int.from_bytes(r[(0x94 + (numVivos * 16) + (i * 4)):(0x94 + (numVivos * 16) + (i * 4) + 4)], "little")
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
                    try:
                        teams[teamN]["name"] = eNames[int.from_bytes(r[(0x46 + shift):(0x48 + shift)], "little") - nameDiff]
                    except IndexError:
                        teams.pop(teamN)
                        continue
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

curr = teamList[0]

def makeLayout():
    global curr

    layout = [
        [ psg.Text("Team File:"), psg.DropDown(teamList, key = "file", default_value = curr), psg.Button("Load", key = "load") ],
        [ psg.Text("Name:"), psg.DropDown(eNames, key = "name", default_value = teams[curr]["name"]) ],
        [ psg.Text("Fighter Rank:"), psg.Input(default_text = teams[curr]["rank"], key = "rank", size = 5, enable_events = True) ],
        [ psg.Text("Battle Points:"), psg.Input(default_text = teams[curr]["points"], key = "points", size = 5, enable_events = True) ],
        [ psg.Text("# of Vivos:"), psg.Input(default_text = teams[curr]["numVivos"], key = "number", size = 5, enable_events = True) ]
    ]
    for i in range(teams[curr]["numVivos"]):
        row = [ # yes, I know this is formatted as a column ulol
            psg.Text("Vivosaur:"),
            psg.DropDown(vNames, key = "vivo", default_value = vNames[teams[curr]["vivos"][i]["vivoNum"]]),
            psg.Text("Level:"),
            psg.Input(default_text = teams[curr]["vivos"][i]["level"], key = "level", size = 5, enable_events = True)
        ]
        if (rom == "ffc"):
            row = row + [
                psg.Text("Super Fossil:"),
                psg.DropDown(sfList, key = "superF", default_value = teams[curr]["vivos"][i]["superName"]),
                psg.Text("SF Points:"),
                psg.Input(default_text = teams[curr]["vivos"][i]["superPoints"], key = "superP", size = 5, enable_events = True)
            ]
        else:
            row = row + [
                psg.Text("AI Set:"),
                psg.Input(default_text = teams[curr]["vivos"][i]["cpu"], key = "cpu", size = 10, enable_events = True)
            ]
        layout = layout + [row]
    layout = layout + [[ psg.Button("Save File", key = "save"), psg.Button("Rebuild ROM", key = "rebuild") ]]
    return(layout)

res = makeLayout()
window = psg.Window("", res, grab_anywhere = True, resizable = True, font = "-size 12")

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "load"):
        curr = values["file"]
        window.close()
        res = makeLayout()
        window = psg.Window("", res, grab_anywhere = True, resizable = True, font = "-size 12")
    if (event == "rebuild"):
        subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
        psg.popup("You can now play out.nds!", font = "-size 12")
        break
    