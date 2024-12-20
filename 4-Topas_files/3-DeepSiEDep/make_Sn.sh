#!/bin/bash

# Define the source directory and the new directories
source_dir="2.0mm_TiBU"
new_dirs=("0.1mm_SnBU" "0.5mm_SnBU" "1mm_SnBU" "2.0mm_SnBU")
source_dirs=("0.1mm_TiBU" "0.5mm_TiBU" "1mm_TiBU" "2.0mm_TiBU")

ii=0
# Create the new directories and copy the contents
for new_dir in "${new_dirs[@]}"; do
    # Create the new directory
    mkdir -p "$new_dir"
    
    # Copy the contents from the source directory to the new directory
    cp -r "${source_dirs[$ii]}"/* "$new_dir/"
    
    # Replace "Ti" with "W" in the filenames and contents
    for file in "$new_dir"/*; do
        # Rename the file if it contains "Ti"
        if [[ "$file" == *"Ti"* ]]; then
            new_file="${file//Ti/W}"
            mv "$file" "$new_file"
            file="$new_file"
        fi
        
        # Replace "Ti" with "W" in the file contents
        sed -i 's/_Ti/_Sn/g' "$file"
    done
    # increase the counter
    ii=$((ii+1))
    echo "Created and modified $new_dir"
done