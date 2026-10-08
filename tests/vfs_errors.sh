#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs tests/vfs/missing.csv --script tests/emu/vfs_info.txt
./run.sh --vfs tests/vfs/bad_base64.csv --script tests/emu/vfs_info.txt
./run.sh --vfs tests/vfs/bad_type.csv --script tests/emu/vfs_info.txt
