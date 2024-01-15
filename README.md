# Fossil-Fighters-Teams-Editor
This is a simple graphical editor for FF1 and FFC teams. Note that, currently, editing certain FFC teams in certain ways will cause
crashes. I have absolutely no idea how to fix it (hence why FFC team randomization is unavailable); it is only an option here to save
me time later.

To use, just drag and drop a ROM onto teams.exe. If the folder NDS_UNPACK does not exist, it will make that folder and unpack the ROM
into it; be patient as it does so (especially for FFC). Then, you can use the editor. It should be mostly self-eplanatory, but please
note the following:
- Only the top list, of file names, changes which file you go to (even I get confused and try to change via fighter name). The reason
  for this is, well, a majority of the fighters are named "Fossil Fighter", so it's both easier to implement and less confusing to go
  by file name
- To get an easier grasp on which files are which, check out "FF1 Teams.txt" and "FFC Teams.txt", which list out the information of
  all team files (in vanilla) in a human-readable format
- Only the Save and Rebuild buttons actually save the file. Apply only changes the data in the editor, while Load does not change
  anything at all (but it does therefore retain your changes in the editor)
  
Also, as with my other tools, the ROM file MUST be in the same folder as teams.exe, or it will not work correctly.
  
To download this, if you are confused, press the Green "Code" button in the top right, then choose "Download ZIP."

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl
