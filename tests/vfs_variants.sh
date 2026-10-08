#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs tests/vfs/min.csv --script tests/emu/vfs_info.txt
./run.sh --vfs tests/vfs/several.csv --script tests/emu/vfs_info.txt
./run.sh --vfs tests/vfs/nested.csv --script tests/emu/vfs_info.txt
