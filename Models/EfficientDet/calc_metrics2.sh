#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

pred_dir=$1
gt_dir=$2
output_dir=$3

# check if the Pred directory exists and it is provided
if [ -z "$pred_dir" ]; then

  echo -e "${red}Error! Train directory not set${reset}"
  exit 1

elif [ ! -d "$pred_dir" ]; then

  echo -e "${red}Error! Train directory not found${reset}"
  exit 1

fi

# check if the Ground_truth directory exists and it is provided
if [ -z "$gt_dir" ]; then

  echo -e "${red}Error! Train directory not set${reset}"
  exit 1

elif [ ! -d "$gt_dir" ]; then

  echo -e "${red}Error! Train directory not found${reset}"
  exit 1

fi

# check if the Output directory is provided
if [ -z "$output_dir" ]; then

  echo -e "${red}Error! Output directory not set${reset}"
  exit 1

fi

# process metrics.py
python3 -m CTLungSeg.metrics2 -pred_folder="$pred_dir" -gt_folder="$gt_dir" -output_folder="$output_dir"