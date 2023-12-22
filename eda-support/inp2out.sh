#!/bin/bash

input_folder="/path/to/eda-support/input"
output_folder="/path/to/eda-support/output"

cd "$input_folder"

for input_file in *.inp; do
    filename_no_ext="${input_file%.inp}"

    /home/rkdql/gamess-21r2/gamess/rungms "$input_file" >& "$output_folder/$filename_no_ext.log"

    sleep 1
done

# 계산 후 *.dat 파일 제거
# rm /path/to/gamess/scr/*.dat
