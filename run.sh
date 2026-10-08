#!/bin/sh
dir=$(dirname "$0")
PYTHONPATH="$dir/src" exec python3 "$dir/src/main.py" "$@"
