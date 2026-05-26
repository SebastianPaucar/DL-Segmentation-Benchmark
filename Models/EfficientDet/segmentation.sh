#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

input_dir=$1
output_dir=$2
is_CPU=$3

# check if the input and output directories exist and they are provided
if [ -z "$input_dir" ]; then

  echo -e "${red}Error! Input directory not set${reset}"
  exit 1

elif [ ! -d "$output_dir" ]; then

  echo -e "${red}Error! Output directory not found${reset}"
  exit 1

fi

alt_output_dir="./Examples/ALL_OUTPUT/"

mkdir -p $alt_output_dir

if [ "$is_CPU" ]; then
  medpseg_cpu --i "$input_dir" --o "$alt_output_dir" --disable_lobe
else
  medpseg --i "$input_dir" --o "$alt_output_dir" --disable_lobe
fi

./ggo_extraction.sh -alt_output_dir "$alt_output_dir" -output_dir "$output_dir"

