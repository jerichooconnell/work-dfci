import os
import sys
import glob
import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
from numpy import unique


def bin_to_array(fn, num_bytes=32, pix_width=512):

    if num_bytes == 32:
        dtype = np.float32
    elif num_bytes == 64:
        dtype = np.float64

    image = np.fromfile(fn, dtype=dtype)
    num_slices = int(image.shape[0]/(pix_width**2))
    image = image.reshape(num_slices, pix_width, pix_width)

    return image


def parse_attenuation_coefficients(file_path):
    # Open the file and read the lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize an empty dictionary to store the results
    coefficients = {}

    # Iterate over the lines
    for ii, line in enumerate(lines):
        # Check if the phrase 'Linear Attenuation Coefficients (1/pixel):
        if 'Linear Attenuation Coefficients (1/pixel):' in line:
            print('Found the attenuation coefficients!')
            # If not, print an error message and return the empty dictionary
            # Split the line into words
            for line2 in lines[ii+1:]:
                words = line2.split()
                # print(words)
                # If the line contains an attenuation coefficient
                if len(words) > 2:
                    # Find which word is the equal sign
                    equals_index = words.index('=')

                    # The material is the first word
                    material = words[0]
                    print(material)

                    # The coefficient is the second word, converted to a float
                    coefficient = float(words[equals_index+1])

                    # Add the material and coefficient to the dictionary
                    coefficients[material] = coefficient
                else:
                    break
            break
    return coefficients


# %%
# Load attenuation coeffs in patient
ct_fn, pw = '/home/jericho/Software/sysiphus_drive/XCAT-phantom/DXCAT2/512_female_head_phantom_full_atn_1.bin', 512
# Replace with your file path
file_log = '/home/jericho/Software/sysiphus_drive/XCAT-phantom/DXCAT2/512_female_head_phantom_full_log'
out_file = 'test/mhd_file_test'
ct_scan = bin_to_array(ct_fn, pix_width=pw)
coefficients = parse_attenuation_coefficients(file_log)
coefficients['Air'] = 0
print(coefficients)


# Create a dict and parse the log file to find these values
'''
 pixel width =  0.0500 (cm/pixel)
 slice width =  0.3125 (cm/pixel)
 voxel volume (pixel width^2)(slice_width) =  0.000781 ml
 array_size = 512
 subvoxel_index = 1 => 1 subvoxels per voxel
 starting slice number    = 445
 ending slice number      = 530
'''
with open(file_log, 'r') as file:
    lines = file.readlines()
    for line in lines:
        if 'pixel width =' in line:
            pixel_width = float(line.split('=')[1].split('(')[0])
        if 'slice width =' in line:
            slice_width = float(line.split('=')[1].split('(')[0])
        if 'array_size =' in line:
            array_size = int(line.split('=')[1])
        if 'starting slice number' in line:
            start_slice = int(line.split('=')[1])
        if 'ending slice number' in line:
            end_slice = int(line.split('=')[1])

# Write a mhd header file using the above values that looks like this:
'''
ObjectType = Image
NDims = 3
BinaryData = True
BinaryDataByteOrderMSB = False
DimSize = 526 526 400
ElementSpacing = 0.500 0.500 0.500
ElementType = MET_INT
ElementDataFile = Catphan604.raw
'''

with open(out_file + '.mhd', 'w') as file:
    file.write('ObjectType = Image\n')
    file.write('NDims = 3\n')
    file.write('BinaryData = True\n')
    file.write('BinaryDataByteOrderMSB = False\n')
    file.write('DimSize = {} {} {}\n'.format(
        array_size, array_size, end_slice-start_slice+1))
    file.write('ElementSpacing = {} {} {}\n'.format(
        10*pixel_width, 10*pixel_width, 10*slice_width))
    file.write('ElementType = MET_SHORT\n')
    file.write('ElementDataFile = ' + out_file.split('/')[-1] + '.raw\n')

# Print the contents of the mhd file
print('\n\nContents of the mhd file:\n')
with open(out_file + '.mhd', 'r') as file:
    print(file.read())
# %%
materials = ct_scan.copy()

for ii, material in enumerate(unique(ct_scan)):
    materials[ct_scan == material] = ii

np.array(materials, dtype=np.int16).tofile(out_file + '.raw')

# %%
data_dict = {
    "Air": "G4_AIR.csv",
    "Body": "G4_TISSUE_SOFT_ICRP.csv",
    "Muscle": "G4_MUSCLE_SKELETAL_ICRP.csv",
    "Adipose": "G4_ADIPOSE_TISSUE_ICRP.csv",
    "Lung": "G4_LUNG_LD_ICRP.csv",
    "Spine": "C4_Vertebra_ICRP.csv",
    "Rib": "RIB_BONE_ICRP.csv.csv",
    "Blood": "G4_BLOOD_ICRP.csv",
    "Heart": "HEART_ICRP.csv",
    "Kidney": "SPLEEN_ICRP.csv",
    "Liver": "LIVER_ICRP.csv",
    "Lymph": "LYMPH_ICRP.csv",
    "Pancreas": "PANCREAS_ICRP.csv",
    "Spleen": "SPLEEN_ICRP.csv",
    "Intestine": "INTESTINE_ICRP.csv",
    "Skull": "G4_BONE_CORTICAL_ICRP.csv",
    "Cartilage": "CARTILAGE_ICRP.csv",
    "Brain": "G4_BRAIN_ICRP.csv",
    "Iodine blood": "G4_BLOOD_ICRP.csv",
    "Skin": "G4_SKIN_ICRP.csv",
    "Eye": "G4_EYE_LENS_ICRP.csv",
    "Ovary": "OVARY_ICRP.csv",
    "Red": "RED_MARROW_ICRP.csv",
    "Yellow": "YELLOW_MARROW_ICRP.csv",
    "Testis": "G4_TESTIS_ICRP.csv",
    "Thyroid": "THYROID_ICRP.csv",
    "Bladder": "BLADDER_ICRP.csv",
}

# Find the unique materials in the ct_scan
unique_coefficients = unique(ct_scan)
unique_materials = []

# Loop through the unique coefficients and find the corresponding material
for ii, coefficient in enumerate(unique_coefficients):
    # Find the material that has the closest coefficient value
    closest_material = min(
        coefficients, key=lambda x: abs(coefficients[x]-coefficient))
    print('Closest material to {} is {}'.format(coefficient, closest_material))
    # Replace the coefficient value with the material name
    unique_materials.append(closest_material)

print(unique_coefficients)
print(unique_materials)
# %%
# Make a list that has 3 entries for each material, the material name, the mu value, and the csv file name
mat_list = []
for ii, material in enumerate(unique_materials):
    mat_list.append([])
    mat_list[ii].append(material)
    mat_list[ii].append(data_dict[material].split('.')[0])
    mat_list[ii].append(coefficients[material])

# Now sort the list using the coefficient values
mat_list.sort(key=lambda x: x[2])

# Write a range file in the following format for all the materials in the mat_list
'''
0 0 Air
1 1 polyurethane 
2 2 teflon 
3 3 pmp 
4 4 bone50 
5 5 ldpe 
6 6 polystyrene 
7 7 acrylic 
8 8 bone20 
9 9 pom
'''

with open(out_file + '_range' + '.txt', 'w') as file:
    for ii, mat in enumerate(mat_list):
        file.write('{} {} {}\n'.format(ii, ii, mat[1]))

# Print the contents of the range file
print('\n\nContents of the range file:\n')
with open(out_file + '_range' + '.txt', 'r') as file:
    print(file.read())
