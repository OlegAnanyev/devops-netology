#!/bin/bash
# display command line options

count=1
for param in "$@"; do
    echo "Parameter: $param" на echo "Next parameter: $param"
    count=$(( $count + 1 ))
done

echo "====="
