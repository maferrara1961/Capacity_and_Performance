#!/usr/bin/env bash
set -eu

python3 -m unittest discover -s Tests -p '*Test.py'
