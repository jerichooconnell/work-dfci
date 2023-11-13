import matplotlib.pyplot as plt 
import numpy as np
import mpl_interactions as pli
from read_in_data import load_itk

import argparse
from ggems import *

# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
  prog='image_viewer.py',
  description='''-->> 6 - OpenGL Visualization Example <<--''',
  epilog='''''',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-i', '--image', required=False, default='run_1e10.mhd', help='first image')

args = parser.parse_args()

ggems_image, origin, space = load_itk(args.image) # What is this in? - Should be MeV as well according to didier

plt.figure()
plt.imshow(ggems_image.squeeze())
plt.show(block=True)