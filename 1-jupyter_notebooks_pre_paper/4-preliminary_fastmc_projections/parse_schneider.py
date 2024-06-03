from pprint import pprint
import numpy as np

# Open the file
with open('HUtoMaterialSchneider.txt', 'r') as f:
    lines = f.readlines()

# Initialize dictionaries to hold the variables
iv_dict = {}
uv_dict = {}
sv_dict = {}
dv_dict = {}

# Process each line
for line in lines:
    # Split the line into parts
    parts = line.split('=')
    if len(parts) == 0:
        continue
    # Check the type of the variable
    if parts[0][:3] == 'iv:':
        # Integer variable
        name = parts[0].split(r'/')[-1]
        vals = parts[1].split()
        values = vals[1:]
        iv_dict[name] = values
    elif parts[0][:3] == 'uv:':
        # float vector
        name = parts[0].split(r'/')[-1]
        vals = parts[1].split()
        values = vals[1:]
        uv_dict[name] = values
    elif parts[0][:3] == 'sv:':
        # string vector
        name = parts[0].split(r'/')[-1]
        vals = parts[1].split()
        values = vals[1:]
        sv_dict[name] = values
    elif parts[0][:3] == 'dv:':
        # double vector
        name = parts[0].split(r'/')[-1]
        vals = parts[1].split()
        values = vals[1:]
        dv_dict[name] = values
# pretty print the dictionaries using pretty print function
pprint(iv_dict)
pprint(uv_dict)
pprint(sv_dict)
