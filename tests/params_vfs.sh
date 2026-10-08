#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
./run.sh
./run.sh --vfs tests/vfs/min.csv
