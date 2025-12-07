#!/usr/bin/env bash
set -euo pipefail

SRC_FILE="src/TSWEEP.DO"
DIST_DIR="dist"
ASCII_DIR="$DIST_DIR/ascii_packed"
TOKEN_DIR="$DIST_DIR/tokenized_packed"
TOOLS_DIR="tools/model100-basic-tools/src"

mkdir -p "$ASCII_DIR" "$TOKEN_DIR"

COMPACT_OUT="$ASCII_DIR/TSWEEP.DO"
TOKENIZED_OUT="$TOKEN_DIR/TSWEEP.BA"

echo "Using source: $SRC_FILE"
echo "Tools repo: $TOOLS_DIR"

python "$TOOLS_DIR/pack_basic.py" "$SRC_FILE" "$COMPACT_OUT"
python "$TOOLS_DIR/tokenize_basic.py" "$COMPACT_OUT" "$TOKENIZED_OUT" 0x8001

echo "Created artifacts:"
find "$DIST_DIR" -maxdepth 2 -type f -print
