# TextSweeper

## Overview
An implementation of Minesweeper for the TRS-80 Model 100 in BASIC. Utilizes a 36 by 8 area of the screen to represent the minefield.



### Hardware supported:   
- TRS-80 Model 100   
- Tandy 102   
- Tandy 200   
- TRS-80 Disk/Video Interface (DVI)   

### Controls:

| Key | Action |
| --- | ------ |
| WASD / Arrow Keys | Move the cursor around the minefield |
| F | Set or Unset the Flag on a tile |
| Spacebar / Enter | Check a tile for a mine, or reveal adjacent tiles for a satisfied tile |
| H | Bring up the help screen (Model 100/102 only) or return to game |
| F8 | Exit to MENU |

### Difficulty Options:

| Setting | # of Mines | Minefield Density |
| ------- | ---------- | ----------------- |
| Easy | 30 | 11.72% |
| Medium | 46 | 17.97% |
| Hard | 52 | 20.31% |
| Classic | 36 | 14.06% |
| Custom | 10-217 | ?% | 

## Files
### src/
- TSWEEP.DO - Original source code for Text Sweeper. All comments and original formatting are included.

### ascii_packed/
- TSWEEP.DO - Text source, compressed and renumbered using ROM2/Cleuseau. All comments are removed to minimize size. If transfering using TELCOM, use this version.

### tokenized_packed/
- TSWEEP.BA - Tokenized version of TSWEEP.DO found in ascii_packed/. If transferring using mComm, DeskLink and other methods that load files directly into the filesystem, use this version.

### assembly_subroutines/
- Assembly_tester.ipynb - A Jupyter Notebook written in Python. Used as a utility to convert already assembled hex code into decimal, for the purpose of injecting into BASIC in DATA statements
- CALC_BOUND.8085.ASM - A subroutine that is used to calculate the x,y boundaries used to search for adjacent mines.
- GENERATE_TILE_ARRAY.8085.ASM - A subroutine that is used to populate an array with all initial valid mine positions (x,y)
- TEST_FIND_OFFSET.8085.ASM - A subroutine that returns the index of the nth valid mine position in the array.

