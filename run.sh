#!/usr/bin/env bash

source venv/bin/activate
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Equation: $line"
    python computor.py "${line}"
    echo ""
done < "$1"
