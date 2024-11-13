import os
import FreeSimpleGUI as psg
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
    nameDiff = 0x104E

f = open(rom + "_enemyNames.txt", "rt")
eNames = list(f.read().split("\n"))
f.close()
for i in range(len(eNames)):
    eNames[i] = eNames[i] + " (" + str(i + nameDiff).zfill(4) + ")"

f = open(rom + "_vivoNames.txt", "rt")
vNames = list(f.read().split("\n"))
f.close()
vNamesAlph = vNames.copy()
vNamesAlph.sort()
vNames = ["NONE"] + vNames

formList = ["< (Cambrian)", "> (Jurassic)"]
sfTable = { "0": "NONE", "900": "Silver Head", "901": "Silver Body", "902": "Silver Arms", "903": "Silver Legs", "904": "Gold" }
sfList = list(sfTable.values()).copy()
xpTable = { "0": "0", "410": "9", "1229": "18", "2048": "27", "2867": "36", "3277": "41", "4096": "50" }
xpList = list(xpTable.values()).copy()
moveLevels = [3, 5, 7]
ff1ArenaList = [ "Unused Temple", "Level-Up Arena", "Guhnash", "Hotel/Outside", "Greenhorn/Knotwood", "BB Base/Digadigamid", "Rivet Ravine", 
    "Bottomsup Bay", "Mt. Lavaflow", "Starship", "Secret Island", "Parchment Desert", "Coldfeet Glacier", "Pirate Ship", "Mine Tunnels" ]
ff1MusicTable = { "0": "NONE", "107": "Tutorial", "108": "Captain Travers", "109": "Level-Up (Prelim.)", "110": "Level-Up (Master)",
    "111": "Normal Enemies", "112": "Bosses", "113": "Guhnash", "1303": "Bullwort", "1304": "Dynal" }
ff1MusicList = list(ff1MusicTable.values()).copy()

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
                    bpShift = int.from_bytes(r[4:8], "little")
                    shift = int.from_bytes(r[8:12], "little") - 0x5C
                    teams[teamN]["numVivos"] = r[0x5C + shift]
                    numVivos = teams[teamN]["numVivos"]
                    teams[teamN]["arena"] = ff1ArenaList[r[0x30]]
                    teams[teamN]["required"] = ""
                    firstLen = int.from_bytes(r[0x38:0x3C], "little")
                    secondLen = int.from_bytes(r[0x40:0x44], "little")
                    if (firstLen == secondLen):
                        teams[teamN]["canRequire"] = "Yes"
                    else:
                        teams[teamN]["canRequire"] = "No" # no way I'm letting you try using both kinds of weird data at the end
                    if ((firstLen == secondLen) and (secondLen < len(r))):
                        count = int.from_bytes(r[0x3C:0x40], "little")
                        for i in range(count):
                            teams[teamN]["required"] = teams[teamN]["required"] + str(int.from_bytes(r[(firstLen + (i * 4)):(firstLen + (i * 4) + 4)], "little")) + ", "
                    if (teams[teamN]["required"].endswith(", ") == True):
                        teams[teamN]["required"] = teams[teamN]["required"][0:-2]
                    teams[teamN]["music"] = ff1MusicTable[str(int.from_bytes(r[12:14], "little"))]                    
                    teams[teamN]["points"] = int.from_bytes(r[(0x54 + bpShift):(0x58 + bpShift)], "little")
                    if (teams[teamN]["points"] == 0xFFFFFFFF):
                        teams[teamN]["points"] = 0
                    try:
                        teams[teamN]["name"] = eNames[int.from_bytes(r[(0x64 + shift):(0x66 + shift)], "little") - nameDiff]
                    except IndexError:
                        teams.pop(teamN)
                        continue
                    teams[teamN]["rank"] = r[0x68 + shift]
                    teams[teamN]["vivos"] = [ {}, {}, {} ]
                    for i in range(numVivos):
                        teams[teamN]["vivos"][i]["vivoNum"] = int.from_bytes(r[(0x94 + shift + (i * 12)):(0x94 + shift + (i * 12) + 4)], "little")
                        teams[teamN]["vivos"][i]["level"] = int.from_bytes(r[(0x94 + shift + (i * 12) + 4):(0x94 + shift + (i * 12) + 8)], "little")
                        teams[teamN]["vivos"][i]["superName"] = "NONE"
                        teams[teamN]["vivos"][i]["superPoints"] = 0
                        teams[teamN]["vivos"][i]["cpu"] = int.from_bytes(r[(0x94 + shift + (numVivos * 12) + (i * 4)):(0x94 + shift + (numVivos * 12) + (i * 4) + 4)], "little")
                        try:
                            teams[teamN]["vivos"][i]["unknown"] = xpTable[str(int.from_bytes(r[(0x94 + shift + (numVivos * 16) + (i * 4)):(0x94 + shift + (numVivos * 16) + (i * 4) + 4)], "little"))]
                        except:
                            print(teamN)
                            sys.exit()
                        teams[teamN]["vivos"][i]["fossils"] = int.from_bytes(r[(0x94 + shift + (numVivos * 20) + (i * 4)):(0x94 + shift + (numVivos * 20) + (i * 4) + 4)], "little")
else:
    teams = {}
    for root, dirs, files in os.walk("NDS_UNPACK/data/battle_param/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                if (len(r) > 0x46): # and (r[0x34] == 0):
                    teamN = os.path.join(root, file).split("\\")[-2]
                    teams[teamN] = {}
                    shift = r[0x38] + 2 - 0x46
                    teams[teamN]["numVivos"] = r[0x58 + shift]
                    numVivos = teams[teamN]["numVivos"]
                    teams[teamN]["points"] = int.from_bytes(r[0x30:0x32], "little")
                    if (teams[teamN]["points"] == 0xFFFF):
                        teams[teamN]["points"] = 0
                    teams[teamN]["rank"] = r[0x48 + shift]
                    teams[teamN]["formation"] = formList[r[0x4C + shift]]
                    teams[teamN]["vivos"] = [ {}, {}, {} ]
                    for i in range(numVivos):
                        teams[teamN]["vivos"][i]["vivoNum"] = int.from_bytes(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)], "little")
                        teams[teamN]["vivos"][i]["level"] = int.from_bytes(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)], "little")
                        teams[teamN]["vivos"][i]["superName"] = sfTable[str(int.from_bytes(r[(0x70 + shift + (i * 12) + 6):(0x70 + shift + (i * 12) + 8)], "little"))]
                        teams[teamN]["vivos"][i]["superPoints"] = int.from_bytes(r[(0x70 + shift + (i * 12) + 8):(0x70 + shift + (i * 12) + 10)], "little")
                        teams[teamN]["vivos"][i]["cpu"] = 0
                        teams[teamN]["vivos"][i]["unknown"] = int.from_bytes(r[(0x70 + shift + (numVivos * 12) + (i * 4)):(0x70 + shift + (numVivos * 12) + (i * 4) + 4)], "little")
                        teams[teamN]["vivos"][i]["fossils"] = int.from_bytes(r[(0x70 + shift + (numVivos * 16) + (i * 2)):(0x70 + shift + (numVivos * 16) + (i * 2) + 2)], "little")
                    try:
                        orig = int.from_bytes(r[(0x46 + shift):(0x48 + shift)], "little")
                        teams[teamN]["name"] = eNames[orig - nameDiff]
                        teamList.append(teamN)
                    except IndexError:
                        teams.pop(teamN)
    teamList.sort(key = lambda x: x.split("_")[-1].zfill(4))

curr = teamList[0]

def makeLayout():
    global curr
    global teams

    layout = [
        [ psg.Text("Team File:"), psg.DropDown(teamList, key = "file", default_value = curr), psg.Button("Load", key = "load") ],
        [ psg.Text("Name:"), psg.DropDown(eNames, key = "name", default_value = teams[curr]["name"]) ],
        [ psg.Text("Fighter Rank:"), psg.Input(default_text = str(teams[curr]["rank"]), key = "rank", size = 5, enable_events = True) ],
        [ psg.Text("Battle Points:"), psg.Input(default_text = str(teams[curr]["points"]), key = "points", size = 5, enable_events = True) ],
        [ psg.Text("# of Vivos:"), psg.DropDown(["1", "2", "3"], key = "number", default_value = str(teams[curr]["numVivos"])),
            psg.Button("Apply", key = "apply") ]
    ]
    if (rom == "ffc"):
        formRow = [[ psg.Text("Formation:"), psg.DropDown(formList, key = "formation", default_value = teams[curr]["formation"]) ]]
        layout = layout[0:4] + formRow + layout[4:]
    else:
        arenaRow = [[ psg.Text("Arena:"), psg.DropDown(ff1ArenaList, key = "arena", default_value = teams[curr]["arena"]) ]]
        musicRow = [[ psg.Text("Music:"), psg.DropDown(ff1MusicList, key = "music", default_value = teams[curr]["music"]) ]]
        requireRow = [[ psg.Text("Req'd:"), psg.Input(default_text = teams[curr]["required"], key = "required", size = 10, enable_events = True) ]]
        layout = layout[0:2] + arenaRow + musicRow + layout[2:]
        if (teams[curr]["canRequire"] == "Yes"):
            layout = layout[0:4] + requireRow + layout[4:]
    for i in range(teams[curr]["numVivos"]):
        # print(i)
        row = [ # yes, I know this is formatted as a column ulol
            psg.Text("Vivosaur:"),
            psg.DropDown(vNamesAlph, key = "vivo" + str(i), default_value = vNames[teams[curr]["vivos"][i]["vivoNum"]]),
            psg.Text("Level:"),
            psg.Input(default_text = str(teams[curr]["vivos"][i]["level"]), key = "level" + str(i), size = 5, enable_events = True),
        ]
        if (rom == "ffc"):
            row = row + [
                psg.Text("Super Fossil:"),
                psg.DropDown(sfList, key = "superF" + str(i), default_value = teams[curr]["vivos"][i]["superName"]),
                psg.Text("SF Points:"),
                psg.Input(default_text = teams[curr]["vivos"][i]["superPoints"], key = "superP" + str(i), size = 5, enable_events = True)
            ]
            row = row + [
                psg.Text("Unknown:"),
                psg.Input(default_text = teams[curr]["vivos"][i]["unknown"], key = "unknown" + str(i), size = 5, enable_events = True)
            ]
        else:
            row = row + [
                psg.Text("Fossils:"),
                psg.DropDown(["1", "2", "3", "4"], key = "fossil" + str(i), default_value = str(teams[curr]["vivos"][i]["fossils"]))
            ]
            row = row + [
                psg.Text("AI Set:"),
                psg.Input(default_text = teams[curr]["vivos"][i]["cpu"], key = "cpu" + str(i), size = 5, enable_events = True)
            ]
            row = row + [ 
                psg.Text("EXP (For LP):"),
                psg.DropDown(xpList, key = "unknown" + str(i), default_value = teams[curr]["vivos"][i]["unknown"], size = 5, enable_events = True)
            ]
        layout = layout + [row]
    layout = layout + [[ psg.Button("Save File", key = "save"), psg.Button("Recompress All", key = "recomp"),
        psg.Button("Rebuild ROM", key = "rebuild") ]]
    return(layout)

def applyValues(values, numChange):
    global curr
    global teams

    teams[curr]["name"] = values["name"]

    if (rom == "ff1"):
        rankMax = 9
        levelMax = 12
    else:
        rankMax = 20
        levelMax = 20
        
    try: # these all need exceptions either to handle non-integers or the buttons not existing for one ROM or the other
        teams[curr]["rank"] = max(1, min(int(values["rank"]), rankMax))
    except:
        pass    
    try:
        teams[curr]["arena"] = values["arena"]
    except:
        pass
    try:
        teams[curr]["music"] = values["music"]
    except:
        pass    
    try:
        teams[curr]["required"] = values["required"]
    except:
        pass
    try:
        teams[curr]["points"] = max(0, int(values["points"]))
    except:
        pass
    try:
        teams[curr]["formation"] = values["formation"]
    except:
        pass 
    
    for i in range(teams[curr]["numVivos"]):
        teams[curr]["vivos"][i]["vivoNum"] = vNames.index(values["vivo" + str(i)])
        try:
            teams[curr]["vivos"][i]["level"] = max(1, min(int(values["level" + str(i)]), levelMax))
        except:
            pass
        try:
            teams[curr]["vivos"][i]["superName"] = values["superF" + str(i)]
        except:
            pass
        try:
            teams[curr]["vivos"][i]["superPoints"] = max(1, min(int(values["superP" + str(i)]), 100))
            if (values["superF" + str(i)] == "NONE"):
                teams[curr]["vivos"][i]["superPoints"] = 0
        except:
            pass
        try:
            teams[curr]["vivos"][i]["cpu"] = max(1, min(int(values["cpu" + str(i)]), 1600))
        except:
            pass
        try:
            teams[curr]["vivos"][i]["unknown"] = str(int(values["unknown" + str(i)]))
        except:
            pass
        try:
            teams[curr]["vivos"][i]["fossils"] = max(1, min(int(values["fossil" + str(i)]), 4))
        except:
            pass
    
    if (numChange == True):
        old = teams[curr]["numVivos"]
        diff = int(values["number"]) - teams[curr]["numVivos"]
        teams[curr]["numVivos"] = int(values["number"])

        if (diff > 0):
            for i in range(old, old + diff):
                temp = { "vivoNum": 0, "level": 1, "superName": "NONE", "superPoints": 0, "cpu": 0, "unknown": 0, "fossils": 1 }
                if (rom == "ffc"):
                    temp["unknown"] = teams[curr]["vivos"][0]["unknown"]
                if (len(teams[curr]["vivos"][i].keys()) == 0):
                    teams[curr]["vivos"][i] = temp.copy()

def saveFile():
    global curr
    global teams

    if (rom == "ff1"):
        path = "NDS_UNPACK/data/battle/bin/" + curr + "/0.bin"
        f = open(path, "rb")
        r = f.read()
        f.close()
        f = open(path, "wb")
        f.close()
        f = open(path, "ab")
        
        bpShift = int.from_bytes(r[4:8], "little")
        shift = int.from_bytes(r[8:12], "little") - 0x5C
        
        f.write(r[0:12])
        for k in ff1MusicTable.keys():
            if (ff1MusicTable[k] == teams[curr]["music"]):
                f.write(int(k).to_bytes(2, "little"))
                break
        f.write(r[14:0x30])
        f.write(ff1ArenaList.index(teams[curr]["arena"]).to_bytes(1, "little"))
        f.write(r[0x31:(0x54 + shift)])
        if (teams[curr]["points"] != 0):
            f.write(teams[curr]["points"].to_bytes(4, "little"))
        else:
            f.write((0xFFFFFFFF).to_bytes(4, "little"))
            
        f.write(r[(0x58 + shift):(0x5C + shift)])
        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write(r[(0x60 + shift):(0x64 + shift)])
        f.write(int(teams[curr]["name"][-5:-1]).to_bytes(4, "little"))
        f.write(teams[curr]["rank"].to_bytes(4, "little"))
        
        numValues = [ [0x44, 0x48, 0x4C, 0x50], [0x50, 0x58, 0x60, 0x68], [0x5C, 0x68, 0x74, 0x80] ]
        ours = numValues[teams[curr]["numVivos"] - 1]

        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write(ours[0].to_bytes(4, "little"))
        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write(ours[1].to_bytes(4, "little"))
        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write(ours[2].to_bytes(4, "little"))
        f.write(r[(0x84 + shift):(0x88 + shift)])
        f.write(ours[3].to_bytes(4, "little"))
        f.write(r[(0x8C + shift):(0x94 + shift)])
        
        for i in range(teams[curr]["numVivos"]):
            f.write(teams[curr]["vivos"][i]["vivoNum"].to_bytes(4, "little"))
            f.write(teams[curr]["vivos"][i]["level"].to_bytes(4, "little"))
            f.write(bytes(4))
        for i in range(teams[curr]["numVivos"]):
            f.write(teams[curr]["vivos"][i]["cpu"].to_bytes(4, "little"))
        for i in range(teams[curr]["numVivos"]):
            for k in xpTable.keys():
                if (xpTable[k] == teams[curr]["vivos"][i]["unknown"]):
                    f.write(int(k).to_bytes(4, "little"))
                    break
        for i in range(teams[curr]["numVivos"]):
            f.write(teams[curr]["vivos"][i]["fossils"].to_bytes(4, "little"))
            
        firstLen = int.from_bytes(r[0x38:0x3C], "little")
        secondLen = int.from_bytes(r[0x40:0x44], "little")
        f.write(r[(firstLen - 8):secondLen])     
        f.close()
        
        size = os.stat(path).st_size
        oldSize = len(r)
        if ((teams[curr]["canRequire"] == "Yes") and (r[0x38] > 0)):
            oldSize = secondLen
        f = open(path, "rb")
        r2 = f.read()
        f.close()
        f = open(path, "wb")
        f.close()
        f = open(path, "ab")
        f.write(r2[0:0x38])
        f.write((firstLen + size - oldSize).to_bytes(4, "little"))
        f.write(r2[0x3C:0x40])
        f.write((secondLen + size - oldSize).to_bytes(4, "little"))
        f.write(r2[0x44:])
        f.close()
        
        if (teams[curr]["canRequire"] == "Yes"):
            reqs = list(teams[curr]["required"].replace(" ", "").replace("\n", "").split(","))
            reqs = list(set(reqs))
            try:
                reqs = [ max(1, min(100, int(x))) for x in reqs ]
            except:
                reqs = []
            reqs = reqs[0:3] # you can only have three vivos on your team, after all
            f = open(path, "rb")
            r3 = f.read()
            f.close()
            f = open(path, "wb")
            f.close()
            f = open(path, "ab")
            f.write(r3[0:0x3C])
            f.write(len(reqs).to_bytes(4, "little"))
            f.write(r3[0x40:])
            for v in reqs:
                f.write(v.to_bytes(4, "little"))
            f.close()

        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle/bin/" + curr, "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/battle/" + curr ])
    else:
        path = "NDS_UNPACK/data/battle_param/bin/" + curr + "/0.bin"
        f = open(path, "rb")
        r = f.read()
        f.close()
        f = open(path, "wb")
        f.close()
        f = open(path, "ab")
        
        f.write(r[0:0x30])
        if (teams[curr]["points"] != 0):
            f.write(teams[curr]["points"].to_bytes(2, "little"))
        else:
            f.write((0xFFFF).to_bytes(2, "little"))
        
        shift = r[0x38] + 2 - 0x46
        f.write(r[0x32:(0x46 + shift)])
        f.write(int(teams[curr]["name"][-5:-1]).to_bytes(2, "little"))
        f.write(teams[curr]["rank"].to_bytes(2, "little"))
        f.write(r[(0x4A + shift):(0x4C + shift)])
        f.write(formList.index(teams[curr]["formation"]).to_bytes(1, "little"))
        f.write(r[(0x4D + shift):(0x50 + shift)])
        
        numValues = [ [0x2C, 0x38, 0x3C, 0x40], [0x2C, 0x44, 0x4C, 0x50], [0x2C, 0x50, 0x5C, 0x64] ]
        ours = numValues[teams[curr]["numVivos"] - 1]
        oldNumVivos = r[0x58 + shift]
        retain = numValues[oldNumVivos - 1][1] - r[0x5C + shift]

        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write(ours[0].to_bytes(4, "little"))
        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write((ours[1] + retain).to_bytes(4, "little"))
        f.write(teams[curr]["numVivos"].to_bytes(4, "little"))
        f.write((ours[2] + retain).to_bytes(4, "little"))
        f.write(r[(0x68 + shift):(0x6C + shift)])
        f.write((ours[3] + retain).to_bytes(4, "little"))
        
        for i in range(teams[curr]["numVivos"]):
            f.write(teams[curr]["vivos"][i]["vivoNum"].to_bytes(2, "little"))
            f.write(teams[curr]["vivos"][i]["level"].to_bytes(4, "little"))
            for k in sfTable.keys():
                if (sfTable[k] == teams[curr]["vivos"][i]["superName"]):
                    f.write(int(k).to_bytes(2, "little"))
                    break
            f.write(teams[curr]["vivos"][i]["superPoints"].to_bytes(4, "little"))
        for i in range(teams[curr]["numVivos"]):
            f.write(int(teams[curr]["vivos"][i]["unknown"]).to_bytes(4, "little"))
        for i in range(teams[curr]["numVivos"]):
            lev = teams[curr]["vivos"][i]["level"]
            fos = 0
            if (lev < moveLevels[0]):
                fos = 1
            elif (lev < moveLevels[1]):
                fos = 2
            elif (lev < moveLevels[2]):
                fos = 3
            else:
                fos = 4
            f.write(fos.to_bytes(2, "little"))
            
        end = len(r)
        if (r[end - 6] == 0):
            f.write(r[(end - 6):end])
        else:
            f.write(r[(end - 4):end])
        f.close()

        size = os.stat(path).st_size
        f = open(path, "rb")
        r2 = f.read()
        f.close()
        f = open(path, "wb")
        f.close()
        f = open(path, "ab")
        f.write(r2[0:0x40])
        f.write(size.to_bytes(4, "little"))
        f.write(r2[0x44:])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle_param/bin/" + curr, "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/battle_param/" + curr ])
    psg.popup("File saved!", font = "-size 12")

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
    elif (event == "apply"):
        applyValues(values, True)
        window.close()
        res = makeLayout()
        window = psg.Window("", res, grab_anywhere = True, resizable = True, font = "-size 12")
    elif (event == "save"):
        applyValues(values, False)
        saveFile()
    elif (event == "rebuild"):
        applyValues(values, False)
        saveFile()
        if (rom == "ff1"):
            shutil.move("NDS_UNPACK/data/battle/bin/", "bin/")
            subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
            shutil.move("bin/", "NDS_UNPACK/data/battle/bin/")
        else:            
            shutil.move("NDS_UNPACK/data/battle_param/bin/", "bin/")
            subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
            shutil.move("bin/", "NDS_UNPACK/data/battle_param/bin/")
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
        psg.popup("You can now play out.nds!", font = "-size 12")
        break
    elif (event == "recomp"):
        applyValues(values, False)
        saveFile()
        if (rom == "ff1"):
            for root, dirs, files in os.walk("NDS_UNPACK/data/battle/bin"):
                for file in files:
                    if (file == "0.bin"):
                        f = open(os.path.join(root, file), "rb")
                        r = f.read()
                        f.close()
                        # if (r[0x3C] > 0):
                            # print(str(r[0x3C]) + "   " + os.path.join(root, file))
                        if (len(r) > 0x94):
                            teamN = os.path.join(root, file).split("\\")[-2]
                            subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle/bin/" + teamN, "-c", "None", "-c",
                                "None", "-i", "0.bin", "-o", "NDS_UNPACK/data/battle/" + teamN ])
        else:
            for root, dirs, files in os.walk("NDS_UNPACK/data/battle_param/bin"):
                for file in files:
                    if (file == "0.bin"):
                        f = open(os.path.join(root, file), "rb")
                        r = f.read()
                        f.close()
                        if (len(r) > 0x46) and (r[0x34] == 0):
                            teamN = os.path.join(root, file).split("\\")[-2]                           
                            subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle_param/bin/" + teamN, "-c", "None", "-c",
                                "None", "-i", "0.bin", "-o", "NDS_UNPACK/data/battle_param/" + teamN ])
        psg.popup("Files recompressed! Don't forget to rebuild!", font = "-size 12")