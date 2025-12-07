# TextSweeper Development Tools

Tools for packing and tokenizing BASIC code for TRS-80 Model 100/102 and Tandy 200 computers.

> Tools are now provided via the `tools/model100-basic-tools` git submodule. Use the scripts in `tools/model100-basic-tools/src/` or run `scripts/build_release.sh` from the repo root.

## Complete Workflow

```
Source Code (.BASIC)
    ↓
model100-basic-tools/src/pack_basic.py      ← Remove comments, merge lines, optimize
    ↓
Packed ASCII (.DO)
    ↓
model100-basic-tools/src/tokenize_basic.py  ← Convert to binary token format
    ↓
Tokenized Binary (.BA) ← Ready for Tandy!
```

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
python model100-basic-tools/src/pack_basic.py src/TSWEEP.DO ascii_packed/TSWEEP.DO
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

---

## tokenize_basic.py

Converts packed ASCII BASIC to tokenized binary format compatible with TRS-80 Model 100, Tandy 102, and Tandy 200 computers.

### Features

- **Complete token table**: 128 keywords + operators + functions (0x80-0xFF)
- **Proper binary format**: [PL PH][LL LH][code][0x00] structure
- **Line pointer calculation**: Correct address computation for jump targets
- **Special case handling**: ELSE token always preceded by colon, single quotes expand properly
- **Byte-for-byte compatibility**: Produces code identical to original Tandy tokenizer

### Usage

```bash
# Model 100/102 (base 0x8001)
python model100-basic-tools/src/tokenize_basic.py input.DO output.BA 0x8001

# Tandy 200 (base 0xA001)
python model100-basic-tools/src/tokenize_basic.py input.DO output.BA 0xA001

# Default (Model 100/102)
python model100-basic-tools/src/tokenize_basic.py input.DO output.BA
```

### How It Works

1. **Parse**: Reads ASCII BASIC line by line
2. **Tokenize**: Converts keywords to single-byte tokens
3. **Special cases**: Handles ELSE (add colon) and quotes (expand)
4. **Structure**: Writes binary format with line headers and terminators
5. **Pointers**: Calculates next-line addresses for all lines

### Token Table

| Range | Type | Examples |
|-------|------|----------|
| 0x80-0x8F | Control Flow | END, FOR, NEXT, GOTO, IF, RETURN, REM, STOP |
| 0x90-0xBF | I/O & Commands | PRINT, INPUT, POKE, CALL, CLS, LOAD, SAVE |
| 0xC0-0xCF | Operators | TO, THEN, AND, OR, NOT, STEP |
| 0xD0-0xDF | Math | +, -, *, /, ^, >, =, <, MOD |
| 0xE0-0xEF | Functions | INT, ABS, SQR, RND, SIN, COS, LOG, EXP, PEEK |
| 0xF0-0xFF | String Funcs | LEN, STR$, VAL, ASC, CHR$, LEFT$, MID$, RIGHT$ |

### Special Cases

- **Single Quote** `'` → `0x3A 0x8E 0xFF` (colon + REM + quote token)
- **ELSE Token** → Always preceded by `0x3A` (colon) if not present
- **Double Quotes** `"` → Preserved as ASCII `0x22`

### Binary File Format

Each tokenized line:
```
Bytes 0-1:   PL PH     (Next line address, little-endian)
Bytes 2-3:   LL LH     (Line number, little-endian)
Bytes 4-N:   Code      (Tokenized BASIC keywords and ASCII)
Byte N+1:    0x00      (Line terminator)
```

### Example

Converting: `CLEAR:VE$="2.7.4"`

```
Source:  CLEAR:VE$="2.7.4"
Tokens:  0xA7  0x3A  ...
Result:  A7 3A (CLEAR keyword + colon)
```

### Platform Support

| Platform | Base Address | Status |
|----------|--------------|--------|
| Model 100 | 0x8001 | ✓ Tested |
| Tandy 102 | 0x8001 | ✓ Compatible |
| Tandy 200 | 0xA001 | ✓ Supported |
| Kyocera Kyotronic-85 | 0x8001 | ✓ Compatible |
| Olivetti M10 | 0x8001 | ✓ Compatible |

### Testing

Validated against original TextSweeper binary:
- ✓ All 80 lines tokenized correctly
- ✓ Code content byte-identical to original
- ✓ File size: 5348 bytes
- ✓ Proper line structure
- ✓ Correct token mappings

### Performance

- Tokenizes 80-line program in ~50ms
- ~67 bytes per line (variable length)
- 60-70% compression vs. ASCII source

### References

- Token format: http://fileformats.archiveteam.org/wiki/Tandy_200_BASIC_tokenized_file
- Tandy 200 reference: Archive Team wiki
- Model 100 docs: "Hidden Powers of the TRS-80 Model 100"
