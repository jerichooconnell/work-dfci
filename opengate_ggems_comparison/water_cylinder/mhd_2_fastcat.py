# This is a script that loads an mhd file and saves it as a fastcat phantom file
# load ipython magic backend and set matplotlib backend to inline

import numpy as np
import SimpleITK as sitk
import fastcat as fc
import matplotlib.pyplot as plt
from mpl_interactions import hyperslicer

# matplotlib.use('Qt5Agg')

# Load the mhd file
mhd_file = sitk.ReadImage('data/Catphan604.mhd')

# Get the image data
image_data = sitk.GetArrayFromImage(mhd_file)

# Get the image spacing
image_spacing = mhd_file.GetSpacing()

# Get the image origin
image_origin = mhd_file.GetOrigin()

# Get the image direction
image_direction = mhd_file.GetDirection()

plt.figure()
pli.pyplot.(image_data[0])
plt.tight_layout()
plt.show()
