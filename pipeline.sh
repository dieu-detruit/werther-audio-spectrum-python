#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./pipeline.sh [letter date (example: 17710512)]"
    exit
else
    date_string=$1
    echo "Target Date: $1"
fi

/usr/bin/env python3 ./scripts/main.py $date_string
