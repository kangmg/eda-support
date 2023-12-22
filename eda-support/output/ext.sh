#!/bin/bash

found=false

for file in *.tar.gz; do
    filename="$file"
    found=true
    tar -xzf "$filename"
done

if [ "$found" == false ]; then
    echo "Cannot find the tar.gz file."
fi

rm -f *.mol *.png *.ctr *.err *.out *.txt *.cmdlog
