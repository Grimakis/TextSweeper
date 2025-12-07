# TextSweeper Development Tools

## pack_basic.py

Python-based BASIC code packer that removes comments, strips whitespace, merges lines, and renumbers for maximum compression. Replaces the need for ROM2/Cleuseau running in a Tandy emulator.

### Features

- **Comment removal**: Strips all comment lines and inline comments
- **Space optimization**: Removes unnecessary spaces (preserves required spaces before AND/OR)
- **Line merging**: Combines non-target lines to reduce line count
- **Smart renumbering**: Renumbers to sequential 1, 2, 3... (saves bytes in tokenized format)
- **Line length enforcement**: Respects 255-character limit for TRS-80 Model 100
- **Reference updating**: Automatically updates all GOTO/GOSUB/THEN/ELSE line number references

### Usage

```bash
python pack_basic.py src/TSWEEP.DO ascii_packed/TSWEEP.DO
```

### Example Output

```
Parsed 144 non-comment lines
Found 41 line number targets
Merged into 56 lines

Line number range: 1-54010 -> 1-56
Line number bytes saved: 647 -> 103 (544 bytes)

Packed: src/TSWEEP.DO -> ascii_packed/TSWEEP.DO
```

### How It Works

1. **Parse**: Reads source file, removes comment-only lines
2. **Find targets**: Identifies all line numbers referenced by GOTO/GOSUB/THEN/ELSE
3. **Pack**: Removes comments and excess spaces from each line
4. **Merge**: Combines consecutive non-target lines with `:` separator
5. **Length check**: Splits lines exceeding 255 characters
6. **Renumber**: Assigns sequential line numbers starting from 1
7. **Update references**: Updates all GOTO/GOSUB/THEN/ELSE to new line numbers

### Notes

- Target lines (referenced by GOTO/GOSUB) cannot be merged
- Lines are merged until they reach ~250 characters (leaving headroom for line number)
- More aggressive than ROM2/Cleuseau (better compression)
- Preserves spaces before AND/OR keywords for BASIC parser compatibility

---

## hex_to_data.py

Converts assembled 8085 machine code (in hexadecimal format) to BASIC DATA statements for embedding in TextSweeper.

### Usage

```bash
# From hex string
python hex_to_data.py "21 C0 FC 01 40 01 7E"

# From file
python hex_to_data.py < assembled_output.hex

# Direct paste
python hex_to_data.py "
    21 C0 FC    ; LXI H, FCC0H
    01 40 01    ; LXI B, 320D
    7E          ; MOV A,M
"
```

### Output

```
DATA 33,192,252,1,64,1,126
Bytes: 7
```

The DATA statement can be copied directly into the BASIC source code.

### Assembly Workflow

1. **Write assembly code** in `.ASM` file (e.g., `CALC_BOUND.8085.ASM`)

2. **Assemble using external tool**:
   - Use an 8085 assembler (ASM80, GNUSim8085, etc.)
   - Output hex or list file with machine code

3. **Copy hex bytes** from assembler output

4. **Convert to DATA statement**:
   ```bash
   python hex_to_data.py "21 C0 FC ..."
   ```

5. **Paste into BASIC**:
   ```basic
   50000 DATA 33,192,252,1,64,1,126,205,68,75,35,11,120,177,194,5,247,201
   ```

6. **Update DIM and POKE statements** in BASIC to load the machine code

### Example: Adding a New Assembly Routine

Say you write a new routine `FAST_COPY.8085.ASM`:

```assembly
    LXI H, FE00H    ; Source
    LXI D, FCC0H    ; Dest
    LXI B, 320D     ; Count
LO: MOV A,M
    STAX D
    INX H
    INX D
    DCX B
    MOV A,B
    ORA C
    JNZ LO
    RET
```

Assemble it and get hex output:
```
21 00 FE 11 C0 FC 01 40 01 7E 12 23 13 0B 78 B1 C2 0A 00 C9
```

Convert to DATA:
```bash
$ python hex_to_data.py "21 00 FE 11 C0 FC 01 40 01 7E 12 23 13 0B 78 B1 C2 0A 00 C9"
DATA 33,0,254,17,192,252,1,64,1,126,18,35,19,11,120,177,194,10,0,201
Bytes: 20
```

Add to BASIC:
```basic
55000 DATA 33,0,254,17,192,252,1,64,1,126,18,35,19,11,120,177,194,10,0,201
55010 DIM FC%(10):FOR N=0 TO 19:READ A%:POKE VARPTR(FC%(0))+N,A%:NEXT:RETURN
```

Then call it:
```basic
CALL VARPTR(FC%(0))
```

## Notes

- The tool strips comments and formatting - only hex bytes are processed
- Hex bytes can be separated by spaces, tabs, or newlines
- Input is case-insensitive
- Labels and symbolic references must be resolved before conversion (done by the assembler)
