# TextSweeper

An implementation of Minesweeper for the TRS-80 Model 100 in BASIC with 8085 assembly subroutines for performance optimization.

[![Version](https://img.shields.io/badge/version-2.7.4-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-Freeware-green.svg)](LICENSE)

## Overview

TextSweeper brings the classic Minesweeper game to the TRS-80 Model 100 and compatible computers. The game features a 32×8 tile minefield displayed on the 40-column or 80-column screen, with optimized assembly routines for smooth gameplay on 1980s hardware.

## Features

- **Multiple difficulty levels**: Easy, Medium, Hard, Classic, and Custom (10-217 mines)
- **Chord reveal**: Click a satisfied tile to reveal all adjacent tiles automatically
- **Hardware optimization**: Assembly subroutines for mine generation and flood-fill operations
- **Multi-platform support**: Works on Model 100, 102, 200, and DVI
- **Responsive controls**: WASD or arrow keys, with configurable flag placement

## Hardware Supported

- TRS-80 Model 100
- Tandy 102
- Tandy 200
- TRS-80 Disk/Video Interface (DVI)
- 40-column and 80-column display modes

## Controls

| Key | Action |
| --- | ------ |
| **WASD** / **Arrow Keys** | Move the cursor around the minefield |
| **F** | Set or unset flag on a tile |
| **Spacebar** / **Enter** | Reveal a tile, or chord reveal adjacent tiles |
| **H** | Bring up help screen (Model 100/102 only) or return to game |
| **F8** | Exit to MENU |

## Difficulty Options

| Setting | Mines | Density |
| ------- | ----- | ------- |
| Easy | 30 | 11.72% |
| Medium | 46 | 17.97% |
| Hard | 52 | 20.31% |
| Classic | 36 | 14.06% |
| Custom | 10-217 | Variable |

## Repository Structure

### Source Code
- **`src/TSWEEP.DO`** - Fully commented source code with original formatting

### Distribution Files
- **`dist/ascii_packed/TSWEEP.DO`** - CI-generated compact ASCII ready for TELCOM
- **`dist/tokenized_packed/TSWEEP.BA`** - CI-generated tokenized binary for mComm/DeskLink

### Assembly Subroutines
Performance-critical routines written in 8085 assembly:

- **`CALC_BOUND.8085.ASM`** - Calculate adjacent tile boundaries
- **`GENERATE_TILE_ARRAY.8085.ASM`** - Generate initial mine pool
- **`SHIFT_VALID_MINES.8085.ASM`** - Adjust mine pool for excluded tiles
- **`LCD_TO_ALTLCD.8085.ASM`** - Copy screen to buffer
- **`ALTLCD_PRINT.8085.ASM`** - Print buffer to screen

### Documentation
- **`docs/VARIABLES.md`** - Comprehensive variable reference
- **`CHANGELOG.md`** - Version history and release notes
- **`LICENSE`** - Freeware license terms

### Tools
- **`tools/model100-basic-tools/`** - Git submodule with the shared packer/tokenizer utilities
- **`tools/Assembly_tester.ipynb`** - Python utility to convert assembled hex to decimal for DATA statements
- **`scripts/build_release.sh`** - Builds compact + tokenized artifacts from `src/TSWEEP.DO`
- **`.github/workflows/release.yml`** - Release workflow that packages and attaches artifacts to GitHub Releases

### Build & Release
- Run `scripts/build_release.sh` to generate `dist/ascii_packed/TSWEEP.DO` and `dist/tokenized_packed/TSWEEP.BA` using the submodule tools.
- The GitHub Actions workflow checks out submodules, runs the build script, uploads the `dist/` artifacts, and attaches them to a published Release.

## Installation

### For TELCOM (Serial Transfer)
1. Use `dist/ascii_packed/TSWEEP.DO` (from CI artifacts or Release downloads)
2. Transfer via serial connection
3. Load and run in BASIC

### For mComm/DeskLink (Direct File Transfer)
1. Use `dist/tokenized_packed/TSWEEP.BA` (from CI artifacts or Release downloads)
2. Copy directly to Model 100 filesystem
3. Run from MENU

## Development

### Assembly Integration
Assembly subroutines are stored as DATA statements in the BASIC code and loaded into memory at runtime. The `tools/Assembly_tester.ipynb` notebook converts assembled machine code to decimal format for embedding in BASIC.

### Memory Layout
- **Screen buffer**: ALTLCD at -832 (M100/102) or -2128 (M200)
- **Assembly routines**: Loaded dynamically into BASIC arrays
- **Game state**: 3D array S%(31,7,2) stores reveal state, flags, and mine counts

See [docs/VARIABLES.md](docs/VARIABLES.md) for complete memory and variable documentation.

## Performance

Version 2.7.4 includes optimizations:
- String conversion optimization (~3% improvement in flood-fill)
- Assembly boundary calculation
- Stack-based flood-fill using ALTLCD buffer

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version**: 2.7.4 (December 2025)

## License

Copyright © 2017-2025 George M. Rimakis. All rights reserved.

This software is provided as **freeware** for personal, non-commercial use. You may use, copy, and distribute the unmodified software freely. Modifications are permitted for personal use only. See [LICENSE](LICENSE) for full terms.

## Author

Created by George M. Rimakis

---

*TextSweeper - Bringing classic puzzle gaming to vintage portable computers since 2017*
