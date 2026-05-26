#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

metrics=$1
carpet=$2

# check if the metrics directory exists and it is provided
if [ -z "$metrics" ]; then

  echo -e "${red}Error! Ground_truth directory not set${reset}"
  exit 1

elif [ ! -d "$metrics" ]; then

  echo -e "${red}Error! Ground_truth directory not found${reset}"
  exit 1

fi


# check if the name of carpet exists and it is provided
if [ -z "$carpet" ]; then

  echo -e "${red}Error! Prediccion directory not set${reset}"
  exit 1

# comment the following lines if the Prediccion directory could not exist
elif [ ! -d "$carpet" ]; then

  echo -e "${red}Error! Prediccion directory not found${reset}"
  exit 1

fi


# list all the pickle files into the prediccion directory
groundTruth_files=$(ls "$ground_truth")
echo "Found ${#groundTruth_files[@]} files to process"

name="metrics_prom_"
ext="csv"
name_csv="$metrics$name$carpet.$ext"

python3 -m CTLungSeg.calc_metrics --path="$metrics"  --output="$name_csv"


if [ "$?" = 0 ]; then
    echo -e "${green}[done]${reset}"
else
    echo -e "${red}[failed]${reset}"
    exit 1 # you can omit this line if you want to catch
           # possible errors into the log without an exit
fi