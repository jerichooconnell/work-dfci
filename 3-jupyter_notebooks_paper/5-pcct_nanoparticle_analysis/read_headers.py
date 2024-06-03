import glob
import os
import shutil
import sys
from pydicom import dcmread


def load_dicom(file_name, header=False):
    # Read the image using pylinac
    ds = dcmread(file_name)
    if header:
        print(ds)
        # exit()
    else:
        pass


def write_dicom_dir(file_name, header=False):
    # Read the image using pylinac
    ds = dcmread(file_name)
    if header:
        print(ds)
        # exit()
    else:
        return ds.SeriesDescription


# Get the directory name from the command line
if len(sys.argv) < 2:
    print("Usage: dicom2png.py <directory>")
    exit()
else:
    directory = sys.argv[1]

# Get the list of files in the directory
files = os.listdir(directory)

series = ''
# # Loop through all the files
# for file in files:
#     # Only process .dcm files
#     if file.endswith(".dcm"):
#         if 'NANO_PARTICLES.CT.UPPER_EXTREMITY.' + series + '.' in file:
#             continue
#         else:
#             print(file + '\n\n')
#             # Read the file
#             load_dicom(os.path.join(directory, file), header=True)
#             # Find the first number in the file path 'NANO_PARTICLES.CT.UPPER_EXTREMITY.3.99.2024.01.31.12.43.30.958.77689692.dcm'
#             series = file.split('.')[3]

for file in files:
    # Only process .dcm files
    if file.endswith(".dcm"):
        if 'NANO_PARTICLES.CT.UPPER_EXTREMITY.' + series + '.' in file:
            continue
        else:
            # print(file + '\n\n')
            # Read the file
            f_discr = write_dicom_dir(
                os.path.join(directory, file), header=False)

            series = file.split('.')[3]
            # print the series description with underscore instead of space
            dir_name = f_discr.replace(' ', '_').replace('#', '')
            # make a directory with the series description
            os.makedirs(os.path.join(directory, dir_name), exist_ok=True)
            # move the file to the new directory
            dcm_files = glob.glob(os.path.join(
                directory, 'NANO_PARTICLES.CT.UPPER_EXTREMITY.' + series + '.*'))
            for dcm_file in dcm_files:
                shutil.move(dcm_file, os.path.join(
                    directory, dir_name, series + '-' + dcm_file.split('/')[-1]))
                print(os.path.join(
                    directory, dir_name, series + '-' + dcm_file.split('/')[-1]))
            # Find the first number in the file path 'NANO_PARTICLES.CT.UPPER_EXTREMITY.3.99.2024.
