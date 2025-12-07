# Changelog

All notable changes to TextSweeper will be documented in this file.

## [2.7.4] - 2025-12-06

### Added
- Comprehensive variable documentation in `docs/VARIABLES.md`
- Documented all BASIC variables, arrays, memory addresses, and naming conventions

### Changed
- Optimized flood-fill display performance (~3% improvement)
- Replaced `RIGHT$(STR$(C),1)` with `CHR$(48+C)` to eliminate string conversion overhead
- Reorganized repository structure:
  - Moved documentation to `docs/` directory
  - Moved Assembly_tester.ipynb to `tools/` directory

### Fixed
- File naming consistency (tokenized file casing)

## [2.7.3] - 2023-11-24

### Changed
- Updated release number

### Fixed
- Stack/Queue refactor improvements
- Moved Stack to ALTLCD buffer
- Fixed display bug on Tandy 200
- Switched Queue to Stack implementation
- Reduced memory footprint to 448 bytes

## [2.7.2] - 2023-11-XX

### Performance
- LCD redraw performance optimization
- Fixed small bug in redraw routine
- Optimized and packed code

## [2.7.0] - 2023-XX-XX

### Added
- Difficulty options: Easy, Medium, Hard, Classic, Custom
- Support for custom mine counts (10-217)

### Changed
- Updated README with difficulty settings

## [2.6.0] - 2023-XX-XX

### Added
- DVI (Disk/Video Interface) support
- 80-column display mode support for DVI
- SCREEN 1 support in DVI

### Fixed
- DVI 80-column print issues
- Exit to MENU instead of BASIC

## [2.5.0] - 2023-XX-XX

### Added
- Tandy 200 support
- Help menu on bottom half of display for T200

### Fixed
- Screen drawing bug on Tandy 200

## [2.4.0] - 2023-XX-XX

### Added
- Help screen (Model 100/102)
- F8 quit to menu
- Tokenized version of file
- WASD control support in addition to arrow keys

### Changed
- Minor UI improvements

## [2.3.0] - 2023-XX-XX

### Added
- Chord reveal feature: selecting a satisfied cell auto-reveals adjacent tiles
- Assembly subroutines for performance-critical operations

### Changed
- Refactored mine placement sequence
- Switched loop counters to integers for performance
- Added key poll to cursor loop

### Fixed
- Win condition bug
- Cursor display during screen drawing
- Flag mine reveal routine

## [2.0.0] - 2023-XX-XX

### Added
- Assembly subroutines:
  - CALC_BOUND.8085.ASM - Calculate adjacent tile boundaries
  - GENERATE_TILE_ARRAY.8085.ASM - Initialize mine pool
  - SHIFT_VALID_MINES.8085.ASM - Mine pool adjustment
  - LCD_TO_ALTLCD.8085.ASM - Screen buffer copy
  - ALTLCD_PRINT.8085.ASM - Buffer to screen print

### Changed
- Major performance improvements using 8085 assembly
- Optimized mine placement algorithm
- Refactored recursive tile reveal
- Store mine locations in index array
- Pre-calculate mine adjacency counts

### Performance
- Print entire rows at once during setup
- Store flag status as integers instead of characters
- Removed unused variables

## [1.0.0] - 2017-XX-XX

### Added
- Initial release
- Basic Minesweeper gameplay
- Support for TRS-80 Model 100 and Tandy 102
- 32×8 minefield
- Cursor controls with arrow keys
- Flag placement with F key
- Spacebar/Enter to reveal tiles

---

**Note:** Dates marked as XX-XX are approximate. Earlier versions did not have detailed release dates tracked.
