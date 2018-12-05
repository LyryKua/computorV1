#!/usr/bin/env bash

bash install.sh
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Equation: $line"
    python computor.py "${line}"
    echo ""
done < "$1"
