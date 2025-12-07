# TextSweeper Development Tools

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
