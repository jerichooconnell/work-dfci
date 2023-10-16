import SimpleITK as sitk
import pydicom
import matplotlib.pyplot as plt

# Load the .mhd file
mhd_file_path = '/home/jericho/Downloads/FastMC/output/projection.mhd'
image = sitk.ReadImage(mhd_file_path)

# Access image information
size = image.GetSize()
spacing = image.GetSpacing()

# Display information
print(f'Image Size: {size}')
print(f'Image Spacing: {spacing}')

plt.figure(figsize=(10,10))
plt.imshow(sitk.GetArrayFromImage(image)[0,:,:],cmap='gray')

image = sitk.GetArrayFromImage(image)[0,:,:]

# Create a function to update the plot based on window and level values
def update_plot(window, level):
    plt.cla()  # Clear the current plot
    vmin = level - window / 2
    vmax = level + window / 2
    plt.imshow(image, cmap='gray', vmin=vmin, vmax=vmax)
    plt.title(f'Window: {window}, Level: {level}')
    plt.colorbar()

# Initial window and level values
initial_window = 1.0
initial_level = 0.5

# Create the interactive plot with sliders
from ipywidgets import interact, FloatSlider
interact(update_plot, window=FloatSlider(min=0.1, max=2.0, step=0.1, value=initial_window),
         level=FloatSlider(min=0.0, max=1.0, step=0.05, value=initial_level))

# save the image directly using pillow
from PIL import Image
im = Image.fromarray(image)
im.save('projection.png')

# open with imagej
import os
os.system('imagej -p 1 rojection.png')