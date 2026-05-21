#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color


npz_dir=$1
npy_dir=$2

# check if the Train directory exists and it is provided
if [ -z "$npz_dir" ]; then

  echo -e "${red}Error! Train directory not set${reset}"
  exit 1

# comment the following lines if the Train directory could not exist
elif [ ! -d "$npz_dir" ]; then

  echo -e "${red}Error! Train directory not found${reset}"
  exit 1

fi

# check if the Ground_truth directory exists and it is provided
if [ -z "$npy_dir" ]; then

  echo -e "${red}Error! Ground_truth directory not set${reset}"
  exit 1


fi

# npz to npy process begins
python3 -m MedSAM.npz_to_npy -npz_dir="$npz_dir" -npy_dir="$npy_dir" -num_workers="4"
