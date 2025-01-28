#!/bin/bash
#!/bin/bash

# Directory containing the Python scripts
dir="/home/jericho/1-Workspace/7-Simulate_Patients_Matt/Pelvis/1-Jupyter_notebooks/./test_gecco_scripts"

# Loop over all Python files in the directory
for file in "$dir"/*.py
do
  # Run the Python file
  python "$file"
done

# Print a message
echo "All Python files in the directory have been run"

