#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

train_dir=$1
ground_truth=$2
output_dir=$3



# check if the Train directory exists and it is provided
if [ -z "$train_dir" ]; then

  echo -e "${red}Error! Train directory not set${reset}"
  exit 1

# comment the following lines if the Train directory could not exist
elif [ ! -d "$train_dir" ]; then

  echo -e "${red}Error! Train directory not found${reset}"
  exit 1

elif [ -d "$train_dir" ]; then
  # total files
  total_files=$(find "$train_dir" -type f | wc -l)
  # Calculate 70% of files
  percent_70=$((total_files * 100 / 100))
fi

# check if the Ground_truth directory exists and it is provided
if [ -z "$ground_truth" ]; then

  echo -e "${red}Error! Ground_truth directory not set${reset}"
  exit 1

elif [ ! -d "$ground_truth" ]; then

  echo -e "${red}Error! Ground_truth directory not found${reset}"
  exit 1

fi

# check if the Output directory exists and it is provided
if [ -z "$output_dir" ]; then

  echo -e "${red}Error! Output directory not set${reset}"
  exit 1

elif [ ! -d "$output_dir" ]; then

  echo -e "${red}Error! Output directory not found${reset}"
  exit 1

fi

# pre process begins
python3 -m MedSAM.pre_CT_MR -img_path="$train_dir" -img_name_suffix="_0000.nii.gz" -gt_path="$ground_truth" -gt_name_suffix=".nii.gz" -output_path="$output_dir" -num_workers="4" -modality="CT" -anatomy="Abd" -window_level="40" -window_width="400" -num_files="$percent_70" --save_nii
