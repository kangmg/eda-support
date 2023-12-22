#!/bin/bash


first_xyz_file=$(ls -1 coordinates/*.xyz | head -n 1)
echo "Your xyz file lines"
echo "-------------------"
awk '{print NR "\t: " $0}' "$first_xyz_file"

echo "line order?  e.g. 1 3 5 2 4 6:"
read system_variable

for  xyz_file in coordinates/*.xyz; do
	python3 source/line_change.py $xyz_file $system_variable
done
