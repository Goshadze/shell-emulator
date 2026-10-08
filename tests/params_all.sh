#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs tests/vfs/min.csv --script tests/emu/ok.txt
