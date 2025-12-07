#!/usr/bin/env bash
set -euo pipefail

SRC_FILE="src/TSWEEP.DO"
DIST_DIR="dist"
TOOLS_DIR="tools/model100-basic-tools/src"

mkdir -p "$DIST_DIR"

COMPACT_OUT="$DIST_DIR/TSWEEP_compact.DO"
TOKENIZED_OUT="$DIST_DIR/TSWEEP_tokenized.BA"

echo "Using source: $SRC_FILE"
echo "Tools repo: $TOOLS_DIR"

python "$TOOLS_DIR/pack_basic.py" "$SRC_FILE" "$COMPACT_OUT"
python "$TOOLS_DIR/tokenize_basic.py" "$COMPACT_OUT" "$TOKENIZED_OUT" 0x8001

echo "Created artifacts:"
ls -l "$DIST_DIR"
