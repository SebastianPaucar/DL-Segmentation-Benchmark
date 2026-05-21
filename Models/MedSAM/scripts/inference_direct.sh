#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

data_dir=$1
pred_save_dir=$2
checkpoint_dir=$3
output_dir=$4


# check if the Data directory exists and it is provided
if [ -z "$data_dir" ]; then

  echo -e "${red}Error! Train directory not set${reset}"
  exit 1

# comment the following lines if the Data directory could not exist
elif [ ! -d "$data_dir" ]; then

  echo -e "${red}Error! Train directory not found${reset}"
  exit 1

fi

# check if the Prediction directory exists and it is provided
if [ -z "$pred_save_dir" ]; then

  echo -e "${red}Error! Prediction directory not set${reset}"
  exit 1

fi

# check if the Checkpoint directory exists and it is provided
if [ -z "$checkpoint_dir" ]; then

  echo -e "${red}Error! Checkpoint file not set${reset}"
  exit 1

elif [ ! -f "$checkpoint_dir" ]; then

  echo -e "${red}Error! Checkpoint file not found${reset}"
  exit 1

fi

# check if the Output directory exists and it is provided
if [ -z "$output_dir" ]; then

  echo -e "${red}Error! Output directory not set${reset}"
  exit 1

fi

# Inference process begins
python3 -m MedSAM.inference_3D_direct -data_root="$data_dir" -pred_save_dir="$pred_save_dir" -medsam_lite_checkpoint_path="$checkpoint_dir" -num_workers="1" --save_overlay -png_save_dir="$output_dir" --overwrite
