#!/bin/bash

html_file="$1"

if [[ ! -f "$html_file" ]]; then
  echo "File not found!"
  exit 1
fi

dir=$(dirname "$html_file")
base_name=$(basename "$html_file" .html)
txt_file="$dir/$base_name.txt"

pandoc -f html -t plain -s "$html_file" -o "$txt_file"
python3 extract_image.py --data_path $html_file 

if [[ $? -eq 0 ]]; then
  echo "Successfully converted $html_file to $txt_file"
else
  echo "Failed to convert $html_file"
fi


