#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

ground_truth=$1
predic_dir=$2
ouput_csv=$3

# check if the Ground_truth directory exists and it is provided
if [ -z "$ground_truth" ]; then

  echo -e "${red}Error! Ground_truth directory not set${reset}"
  exit 1

elif [ ! -d "$ground_truth" ]; then

  echo -e "${red}Error! Ground_truth directory not found${reset}"
  exit 1

fi


# check if the Prediccion directory exists and it is provided
if [ -z "$predic_dir" ]; then

  echo -e "${red}Error! Prediccion directory not set${reset}"
  exit 1

# comment the following lines if the Prediccion directory could not exist
elif [ ! -d "$predic_dir" ]; then

  echo -e "${red}Error! Prediccion directory not found${reset}"
  exit 1

fi


#chck if the ouput_csv file is provided
if [ -z "$ouput_csv" ]; then

  echo -e "${red}Error! Output_csv directory not set${reset}"
  exit 1

# comment the following lines if the output_csv directory could not exist
elif [ ! -d "$ouput_csv" ]; then

  echo -e "${red}Error! Output_csv directory not found${reset}"
  exit 1

fi


# list all the pickle files into the prediccion directory
groundTruth_files=$(ls "$ground_truth")
echo "Found ${#groundTruth_files[@]} files to process"


# apply the pipeline on the input files
for file in $groundTruth_files; do
  printf "* Processing $file ...       "
  # Para extraer el basename del archivo ground truth y crear el nombre del nuevo csv con los resultados
  basename=${file%%.*}
  ext="csv"
  name_csv="$ouput_csv$basename.$ext"
 
  python3 -m CTLungSeg.evaluate --gt="$ground_truth$file"  --pred="$predic_dir$file" --output="$name_csv"

  if [ "$?" = 0 ]; then
    echo -e "${green}[done]${reset}"
  else
    echo -e "${red}[failed]${reset}"
    exit 1 # you can omit this line if you want to catch
           # possible errors into the log without an exit
  fi
  
done