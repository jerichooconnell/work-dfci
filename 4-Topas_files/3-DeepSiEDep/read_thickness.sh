#!/bin/bash

# Define the line number you want to print
line_number=124

# Find all files named run_demo.txt and process them
find . -type f -name "run_demo.txt" | while read -r file; do
    # Get the directory of the file
    dir=$(dirname "$file")
    
    # Print the directory
    echo "Directory: $dir"
    
    # Print the specific line from the file
    sed -n "${line_number}p" "$file"
    
    echo "-----------------------------------"
done