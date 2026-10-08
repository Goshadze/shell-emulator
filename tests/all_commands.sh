#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs tests/vfs/nested.csv --script tests/emu/all.txt
