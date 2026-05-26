#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color

alt_output_dir=$1
output_dir=$2

# check if the input and output directories exist and they are provided
if [ -z "$alt_output_dir" ]; then

  echo -e "${red}Error! Alternative Output directory not set${reset}"
  exit 1

elif [ ! -d "$output_dir" ]; then

  echo -e "${red}Error! Alternative Output directory not found${reset}"
  exit 1

fi

files=$(ls "$alt_output_dir")
echo "Found ${#files[@]} files to process"


# Loop through nii.gz files in the source directory that contain "ggo"
# Loop through nii.gz files in the source directory that contain "ggo"
for file_path in "$alt_output_dir"/*ggo*.nii.gz; do
  # Check if the file name explicitly contains "ggo"
  if [[ $(basename "$file_path") == *"ggo"* ]]; then
    # Extract the filename from the path
    file_name=$(basename "$file_path")
    
    # Extract the base name without the extension
    BaseName_R="${file_name%%.nii.gz}"
    
    # Output the base name
    echo "* Processing $BaseName_R ..."
    
    # Split the base name into components based on underscore (_)
    IFS='_' read -r -a ADDR <<< "$BaseName_R"
    
    # Initialize FinalName to hold the new base name
    FinalName=""
    # Iterate over the array using indices
    for i in "${!ADDR[@]}"; do
      # Append each part to FinalName unless it is "ggo"
      if [[ "${ADDR[i]}" != "ggo" ]]; then
        FinalName+="${ADDR[i]}_"
      fi
    done
    
    # Remove the trailing underscore from FinalName
    FinalName="${FinalName%_}"
    
    # Construct the new file name with the original extension
    NewFileName="${FinalName}.nii.gz"
    
    # Define the full path for the new file
    NewPathName="$output_dir/$NewFileName"
    
    # Move and rename the file
    mv -f "$file_path" "$NewPathName"
    echo "Moved to $NewPathName"
  fi
done