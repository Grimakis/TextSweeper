# TextSweeper BASIC Variables Documentation

This document describes all variables used in TextSweeper, their types, purposes, and valid ranges.

## Game State Variables

### `M`
- **Type:** Integer
- **Purpose:** Minefield generation flag
- **Values:** `0` = mines not generated, `1` = mines generated
- **Used in:** Lines 4000, 4200

### `MC%`
- **Type:** Integer
- **Purpose:** Mine Counter - tracks number of unrevealed non-mine cells remaining
- **Initial Value:** `256 - MN%` (total cells minus mines)
- **Range:** 0 to 226
- **Used in:** Lines 5070, 15100, 17300, 3200
- **Notes:** Decrements on each reveal; when `MC%=0`, player wins

### `MN%`
- **Type:** Integer
- **Purpose:** Number of mines in the game
- **Range:** 10 to 217 (custom) or preset (30, 36, 46, 52)
- **Set in:** Lines 14130 (difficulty presets), 14250 (custom)
- **Used in:** Array dimensioning, loops

## Field Dimensions & Display

### `YO%`
- **Type:** Integer
- **Purpose:** Y Offset - number of columns per row (screen width)
- **Values:** `40` (40-column mode) or `80` (80-column mode)
- **Set in:** Lines 100, 115
- **Used in:** PRINT @ position calculations: `Y*YO%+X`

### `PO%`
- **Type:** Integer
- **Purpose:** Pane Offset - offset for right pane display
- **Values:** `320` (40-col), `640` (40-col alt), `1280` (80-col)
- **Set in:** Lines 110, 115
- **Used in:** Help screen positioning (line 30000 series)

### `AL%`
- **Type:** Integer (negative)
- **Purpose:** ALTLCD buffer start address
- **Values:** `-832` (Model 100/102) or `-2128` (Model 200)
- **Set in:** Line 10
- **Used in:** Stack operations for flood-fill, screen buffering

## Cursor Position

### `X`
- **Type:** Integer
- **Purpose:** Current cursor X coordinate (column)
- **Range:** 0 to 31
- **Initial:** 16 (center of field)
- **Movement:** Lines 3500-3560

### `Y`
- **Type:** Integer
- **Purpose:** Current cursor Y coordinate (row)
- **Range:** 0 to 7
- **Initial:** 3 (center of field)
- **Movement:** Lines 3500-3560

## Loop Counters & Temporary Variables

### `N`, `N%`
- **Type:** Integer
- **Purpose:** General-purpose loop counter
- **Used in:** Multiple loops throughout program
- **Scope:** Local to each loop

### `C`
- **Type:** Integer
- **Purpose:** Adjacent mine count for current cell
- **Range:** 0 to 8
- **Set in:** Line 6010
- **Used in:** Lines 7160-7170 for display

### `TX%`, `TY%`
- **Type:** Integer
- **Purpose:** Temporary X/Y coordinates in loops
- **Range:** TX%: 0-31, TY%: 0-7
- **Used in:** Boundary iteration, adjacency calculation

### `CX%`, `CY%`
- **Type:** Integer
- **Purpose:** Current X/Y from stack during flood-fill
- **Range:** CX%: 0-31, CY%: 0-7
- **Set in:** Line 5060 (popped from stack)
- **Used in:** Lines 5070-8090 for tile revealing

## Stack & Flood-Fill

### `W%`
- **Type:** Integer
- **Purpose:** Stack pointer (write offset into ALTLCD buffer)
- **Range:** 0 to ~512 (grows by 2 per push)
- **Operations:**
  - **Push:** `POKE AL%+W%,X:POKE AL%+W%+1,Y:W%=W%+2`
  - **Pop:** `W%=W%-2:CX%=PEEK(AL%+W%):CY%=PEEK(AL%+W%+1)`
- **Used in:** Lines 5010, 5060, 7300, 8070, 8160, 17020, 17035, 17050

### `FC%`
- **Type:** Integer
- **Purpose:** Flag Count - counts flags around a revealed cell (for chord reveal)
- **Range:** 0 to 8
- **Set in:** Line 17020
- **Used in:** Line 17040 (chord validation)

### `R%`
- **Type:** Integer
- **Purpose:** Reserved/unused (initialized in line 17020)
- **Current Status:** Not actively used

## Mine Generation

### `SE`
- **Type:** Float
- **Purpose:** Random seed from current time
- **Calculation:** `(-3600*seconds) + (-60*minutes) - seconds`
- **Set in:** Line 4020
- **Used in:** Line 4030 for RND initialization

### `DU`
- **Type:** Float
- **Purpose:** Dummy variable for RND seeding
- **Used in:** Line 4030-4040

### `I%`
- **Type:** Integer
- **Purpose:** Random index into mine pool array
- **Range:** 0 to 255
- **Set in:** Line 4065
- **Used in:** Line 4066 (assembly call parameter)

### `I2%`
- **Type:** Integer
- **Purpose:** Output parameter from mine pool assembly routine
- **Returns:** Index of selected mine from available pool
- **Used in:** Lines 4066, 4070

### `J%`
- **Type:** Integer
- **Purpose:** Count of available mine placement positions
- **Range:** Initially 247 (256 - 9 excluded cells), decrements to 247-MN%
- **Used in:** Lines 4017, 4035, 4065

## Arrays

### `S%(31,7,2)`
- **Type:** 3D Integer Array
- **Dimensions:** 32 columns × 8 rows × 3 attributes
- **Size:** 768 elements
- **Declared:** Line 16070
- **Purpose:** Complete game state for each cell

**Index 0 - Reveal State:**
- `0` = Hidden, not queued
- `1` = Hidden, contains mine
- `2` = Revealed, not queued
- `3` = Revealed, contains mine (game over state)
- `+2` modifier = queued for reveal in flood-fill

**Index 1 - Flag/Display State:**
- `0` = Unflagged (shows as 239/CHR$(239))
- `1` = Flagged (shows as 255/CHR$(255))
- `2` = Queued for reveal
- `32` = Revealed as blank (space)
- `48-56` = Revealed with count '0'-'8' (ASCII)

**Index 2 - Mine Adjacency Count:**
- `0` = No adjacent mines
- `1-8` = Number of adjacent mines

### `MI%(MN%-1,1)`
- **Type:** 2D Integer Array
- **Dimensions:** MN% rows × 2 columns
- **Declared:** Line 16076
- **Purpose:** Index of mine coordinates
- **Index 0:** X coordinate (0-31)
- **Index 1:** Y coordinate (0-7)
- **Used in:** Mine placement (4110), mine reveal (12000)

### `MA%(255)`
- **Type:** Integer Array
- **Size:** 256 elements
- **Declared:** Line 51010
- **Purpose:** Mine pool - available positions for mine placement
- **Values:**
  - `-1` = Position excluded or already used
  - `0-255` = Available position (encoded as Y*32+X)
- **Used in:** Lines 4017 (exclude cursor area), 4066 (mine selection), 4110 (mark used)

### `XY%(21)`
- **Type:** Integer Array
- **Size:** 22 elements
- **Declared:** Line 50010
- **Purpose:** Dual-purpose array for CALC_BOUND assembly routine
  - Elements 0-2: Input/output parameters
  - Elements 3+: Assembly code storage
- **Layout:**
  - `XY%(0)` / byte 0: X coordinate (input)
  - `XY%(0)+1` / byte 1: Y coordinate (input)
  - `XY%(1)` / bytes 2-3: X lower/upper bounds (output)
  - `XY%(2)` / bytes 4-5: Y lower/upper bounds (output)
  - `XY%(3)` onwards: Assembly code (38 bytes)

### `MG%(12)`
- **Type:** Integer Array
- **Size:** 13 elements
- **Declared:** Line 51010
- **Purpose:** Mine generation assembly routine storage
- **Layout:**
  - Elements 0-2: Assembly code (start)
  - Element 3: Runtime jump address (updated in line 4013)
  - Elements 4+: Assembly code (continuation)
- **Code Size:** 25 bytes
- **Jump Updates:** Element 7 and 11 (line 4032)

### `TS%(18)`
- **Type:** Integer Array
- **Size:** 19 elements
- **Declared:** Line 52010
- **Purpose:** Tile selection assembly routine (mine pool adjustment)
- **Layout:**
  - Elements 0-14: Assembly code
  - Element 15: Runtime jump address
  - Elements 16-18: Assembly code (continuation)
- **Code Size:** 35 bytes
- **Used in:** Line 4066

### `ME$(6)`
- **Type:** String Array
- **Size:** 7 elements (indices 0-6)
- **Declared:** Line 16077
- **Purpose:** Game end messages
- **Values (line 16078):**
  - `ME$(0)` = "     YOU"
  - `ME$(1)` = "   LOSE!" (changed to "    WIN!" on victory)
  - `ME$(2)` = "        " (blank line)
  - `ME$(3)` = "    Play"
  - `ME$(4)` = "  Again?"
  - `ME$(5)` = "   (Y/N)"
  - `ME$(6)` = "        " (blank line)

## Display & UI Variables

### `VE$`
- **Type:** String
- **Purpose:** Version string
- **Value:** "2.7.3"
- **Used in:** Line 14040 (title screen)

### `CN$`
- **Type:** String
- **Purpose:** Cursor Normal - escape sequence for cursor display
- **Value:** CHR$(27)+CHR$(80)
- **Set in:** Line 14100
- **Used in:** Line 3005 (cursor blink on)

### `CF$`
- **Type:** String
- **Purpose:** Cursor Flash - escape sequence for cursor flash state
- **Value:** CHR$(27)+CHR$(81)
- **Set in:** Line 14100
- **Used in:** Line 3005 (cursor blink off), 24000 (restore)

### `S$`
- **Type:** String
- **Purpose:** Input string for keyboard handling
- **Value:** "Q"+CHR$(28)+CHR$(29)+CHR$(31)+CHR$(30)+CHR$(70)+CHR$(102)+CHR$(32)+CHR$(13)+"WwAaSsDdHh"
- **Encoding:**
  - Position 1: 'Q' (unused placeholder)
  - Position 2-5: Arrow keys (→←↓↑)
  - Position 6-7: 'F', 'f' (flag)
  - Position 8-9: Space, Enter (reveal)
  - Position 10-17: W,w,A,a,S,s,D,d (WASD movement)
  - Position 18-19: H,h (help)
- **Used in:** Line 3020 (INSTR for input routing)

### `H$`
- **Type:** String
- **Purpose:** Help text displayed in right pane
- **Values:** "  [H]elp" (Model 100/102) or "        " (Model 200/DVI)
- **Set in:** Lines 100, 120
- **Used in:** Line 17300

### `LS$`
- **Type:** String
- **Purpose:** Line String - buffer for redrawing bottom row
- **Used in:** Lines 18000-18040
- **Built:** Concatenates 32 characters for row 7

### `T%`
- **Type:** Integer
- **Purpose:** Temporary character code for display
- **Used in:** Lines 18010-18030 (row redraw logic)

### `A$`
- **Type:** String
- **Purpose:** General input buffer
- **Used in:** Yes/no prompts (lines 20000-20040)

### `YN%`
- **Type:** Integer
- **Purpose:** Yes/No response flag
- **Values:** `1` = Yes, `0` = No
- **Set in:** Lines 20020, 20030
- **Used in:** Lines 12270, 23000

## Hardware Detection

### `LD%`
- **Type:** Integer
- **Purpose:** LCD Display type flag
- **Values:**
  - `0` = Model 100/102 (limited display)
  - `1` = Model 200 or DVI (enhanced display)
- **Set in:** Lines 100, 120
- **Used in:** Feature detection (help screen availability, etc.)

## Assembly Code Management

### `A%`
- **Type:** Integer
- **Purpose:** Temporary variable for reading DATA and POKEing assembly code
- **Used in:** Lines 50010, 51010, 52010, 53010, 54010
- **Range:** 0-255 (single byte values)

## Special Values & Constants

### ASCII/Character Codes Used
- `32` = Space (blank revealed cell)
- `42` = '*' (mine character)
- `48-56` = '0'-'8' (mine count digits)
- `239` = CHR$(239) (unflagged cell)
- `255` = CHR$(255) (flagged cell)

### Screen Memory Addresses
- `FE00H` (65024) = LCD screen memory start
- `63211` = LCD_TO_ALTLCD assembly routine
- `63231` = ALTLCD_PRINT assembly routine

### Hardware Detection Memory Locations
- `PEEK(1)` = Model detection (51=M100, 167=M102, 171=M200)
- `PEEK(63035)` = M100/102 display mode
- `PEEK(61190)` = M200 display mode
- `PEEK(63036)` = M100/102 column width
- `PEEK(61191)` = M200 column width
- `PEEK(65339)` = Keyboard buffer check
- `PEEK(65343)` = Help screen state

## Variable Naming Conventions

- **`%` suffix:** Integer type
- **`$` suffix:** String type
- **No suffix:** Float/double type
- **Uppercase:** Persistent game state
- **Mixed case:** Temporary/loop variables
- **Trailing `%`:** Most variables are integers for performance

## Memory Optimization Notes

1. **Integer Usage:** Nearly all variables use `%` (integer) suffix for faster arithmetic on 8085 CPU
2. **Array Reuse:** Assembly code stored in same arrays as parameters (XY%, MG%, TS%)
3. **Stack in ALTLCD:** Reuses screen buffer memory for flood-fill stack to save RAM
4. **String Minimization:** Strings avoided in loops; CHR$ arithmetic preferred over string operations
