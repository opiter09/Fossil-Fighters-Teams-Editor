# Fossil-Fighters-Teams-Editor
This is a simple graphical editor for FF1 and FFC enemy teams.

You MUST put the ROM in the same folder as the exe, or it won't work. Furthermore, this is only designed for Windows. For Mac and
Linux, I can only point you to WINE: https://www.winehq.org. When running this through WINE, please use the command
``wine teams.exe "ROMNAME.NDS"``, not ``wine teams.exe`` alone.

To use, just drag and drop a ROM onto teams.exe. If the folder NDS_UNPACK does not exist, it will make that folder and unpack the
ROM into it; be patient as it does so (especially for FFC). Then, you can use the editor. It should be mostly self-eplanatory,
but please note the following:
- Only the top list of file names changes which file you go to (even I get confused and try to change via fighter name). The reason
  for this is, well, a majority of the fighters are named "Fossil Fighter", so it's both easier to implement and less confusing to go
  by file name
- To get an easier grasp on which files are which, check out "FF1 Teams.txt" and "FFC Teams.txt", which list out the information of
  all team files (in vanilla) in a human-readable format
- The FF1 option "Req'd" refers to vivosaurs you must have on your team to begin the fight. Like with the randomizer's "Post-Game
  Vivos" option, this must be a list of vivosaur Numbers separated by a comma and any number of spaces. The code will automatically
  use the first three values, although this will not be shown in the editor. Finally, some teams do not have this option, due to
  having a different kind of extra data in the same spot
- To avoid cosmetic issues on the Formation screen, enemies' fossils in FFC are assigned automatically, based on the level
  at which moves are learned. In order to accomodate ROMs where these levels are edited, a file named "ffc_moveLevels.txt" is
  generated if none exists. Therefore, if you choose to change levels again, you will need to delete this file in order to
  have the program regenerate it
- Only the Save and Rebuild buttons actually save the file. Apply only changes the data in the editor, while Load does not change
  anything at all (but it does therefore retain your changes in the editor)
- The Recompress All button is for debugging purposes ONLY. It is extremely slow, and should not be necessary unless you are trying
  to help me figure out a problem
  
To download this, if you are confused, press the Green "Code" button in the top right, then choose "Download ZIP".

Finally, many thanks to EchoSpaceZ, for patiently testing this editor and helping me iron out all of the bugs (for FF1 at least).

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl