import matplotlib.pyplot as plt
import numpy as np
import mpl_interactions as pli
import SimpleITK as sitk
from pydicom import dcmread
# from read_in_data import load_itkim
from pylinac.core.image import XIM

import argparse
from ggems import *
import os
import csv


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def load_xim(file_name, header=False):
    # Load the xim File
    if header:
        xim = XIM(file_name, read_pixels=False)
        # write the xim properties to a csv file using csv dict writer
        # Specify the field names from the xim.properties dict as a list
        # Specify the fieldnames for the CSV
        # field_names = list(xim.properties.keys())
        # Print each field name and value
        for key, value in xim.properties.items():
            # Check if the item is a list
            if isinstance(value, tuple):
                # If it is a list, check if the list is longer than 3
                if len(value) > 3:
                    # If it is longer than 3, print the first 3 items
                    print(f"{bcolors.OKGREEN} {key} {bcolors.ENDC}",
                          value[:3], '... len ', len(value))
                else:
                    # If it is shorter than 3, print the whole list
                    print(f"{bcolors.OKGREEN} {key} {bcolors.ENDC}",
                          ' '*(30 - len(key)), value)
            else:
                # If it is not a list, print the value
                print(f"{bcolors.OKGREEN} {key} {bcolors.ENDC}",
                      ' '*(30 - len(key)), value)
        exit()
    else:
        xim = XIM(file_name)
        return xim.array


def load_itk(filename):
    '''
    :param filename: path to the .mhd file
    Returns: ct_scan, origin, spacing
    '''
    # Reads the image using SimpleITK
    itkimage = sitk.ReadImage(filename)

    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    ct_scan = sitk.GetArrayFromImage(itkimage)

    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))

    return ct_scan.squeeze(), origin, spacing


def load_dicom(file_name, header=False):
    # Read the image using pylinac
    ds = dcmread(file_name)
    if header:
        print(ds)
        exit()
    else:
        image = ds.pixel_array
    return image


# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
    prog='image_viewer.py',
    description='''-->> 6 - OpenGL Visualization Example <<--''',
    epilog='''''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-i', '--image', required=False,
                    default='run_1e10.mhd', help='first image')
parser.add_argument('-head', '--header', required=False,
                    default=False, help='first image')

args = parser.parse_args()

if args.image[-4:] == '.mhd':
    # What is this in? - Should be MeV as well according to didier
    ggems_image, origin, space = load_itk(args.image)
elif args.image[-4:] == '.npy':
    ggems_image = np.load(args.image)
elif args.image[-4:] == '.xim':
    ggems_image = load_xim(args.image, args.header)
elif args.image[-4:] == '.dcm':
    ggems_image = load_dicom(args.image, args.header)
else:
    print('File type not supported')
    exit()
plt.figure()
plt.imshow(ggems_image.squeeze(), vmin=np.percentile(
    ggems_image, 1), vmax=np.percentile(ggems_image, 99))
plt.show(block=True)
