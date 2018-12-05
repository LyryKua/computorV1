#!/usr/bin/env bash

if [[ $# -eq 1 ]];
then
    source venv/bin/activate
    while IFS='' read -r line || [[ -n "$line" ]]; do
        echo "Equation: $line"
        python computor.py "${line}"
        echo ""
    done < "$1"
else
    echo "usage: ${0} source_file"
fi
