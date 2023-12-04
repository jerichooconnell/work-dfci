import matplotlib.pyplot as plt 
import numpy as np
import mpl_interactions as pli
import SimpleITK as sitk
# from read_in_data import load_itk

import argparse
from ggems import *

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
# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
  prog='image_viewer.py',
  description='''-->> 6 - OpenGL Visualization Example <<--''',
  epilog='''''',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-i', '--image', required=False, default='run_1e10.mhd', help='first image')

args = parser.parse_args()

if args.image[-4:] == '.mhd':
  ggems_image, origin, space = load_itk(args.image) # What is this in? - Should be MeV as well according to didier
elif args.image[-4:] == '.npy':
  ggems_image = np.load(args.image)
else:
  print('File type not supported')
  exit()
plt.figure()
plt.imshow(ggems_image.squeeze())
plt.show(block=True)