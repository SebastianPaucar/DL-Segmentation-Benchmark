#!/bin/bash

input_dir=$1
output_dir=$2

if [ -z "$input_dir" ]; then
  echo "Error! Input directory not set" >&2
  echo "Set path to input directory" >&2
  exit 1
elif [ ! -d "$input_dir" ]; then
  echo "Error! Input directory not found" >&2
  exit 1
fi

if [ -z "$output_dir" ]; then
  echo "Error! Output directory not set" >&2
  echo "Set path to output directory" >&2
  exit 1
fi

mkdir -p "$output_dir"

files=("$input_dir"/*)
echo "${#files[@]} files found to process"

for file in "${files[@]}"; do
  echo "* Processing $file"
  baseName=$(basename "$file")
  baseName="${baseName%.*}"
  lung_name="$output_dir/$baseName.nii.gz"

  python -m CTLungSeg.convert --input "$file" --output "$lung_name"
  
  if [ $? -eq 0 ]; then
    echo "[done]"
  else
    echo "[failed]"
    exit 1
  fi
done
