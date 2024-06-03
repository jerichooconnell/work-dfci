#!/bin/bash
#!/bin/bash

# Directory containing the Python scripts
dir="./test_python_scripts/"

# Loop over all Python files in the directory
for file in "$dir"/*.py
do
  # Run the Python file
  python "$file"
done
