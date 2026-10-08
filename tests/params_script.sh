#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
./run.sh --script tests/emu/ok.txt
./run.sh --script tests/emu/error.txt
./run.sh --script tests/emu/missing.txt
