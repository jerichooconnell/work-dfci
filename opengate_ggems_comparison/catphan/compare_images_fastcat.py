import SimpleITK as sitk
import numpy as np
import glob
import matplotlib.pyplot as plt
import mpl_interactions as pli

import argparse

# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
    prog='image_viewer.py',
    description='''-->> 6 - OpenGL Visualization Example <<--''',
    epilog='''''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-v', '--vis', required=False, action='store_true', help='Visualize the comparison')

args = parser.parse_args()

def compare_images(image1_path, image2_path):
    # Read the images
    # Reads the image using SimpleITK
    # itkimage1 = sitk.ReadImage(image1_path)

    image1 = np.load(image1_path)
    # image1 = np.flipud(image1)
    image1 = np.fliplr(image1)

    itkimage2 = sitk.ReadImage(image2_path)

    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    # image1 = sitk.GetArrayFromImage(itkimage1)
    image2 = sitk.GetArrayFromImage(itkimage2)

    # Normalize the images
    image1 = standard_scaler(image1)
    image2 = standard_scaler(image2)

    # Calculate and print the statistics
    difference = image1 - image2
    mean_difference = np.mean(difference)
    std_difference = np.std(difference)

    print(f'Mean difference: {mean_difference}')
    print(f'Standard deviation of difference: {std_difference}')

    return image1.squeeze(), image2.squeeze()

def visualize_comparison(image1, image2, file_name1='GGEMS',file_name2='GATE'):

    # Assuming image1 and image2 are your normalized images
    # and they are numpy arrays

    # Display heatmaps
    pli.heatmap_slicer(np.arange(image1.shape[0]),np.arange(image1.shape[1]),
                    [image1, np.rot90(image2,3)], figsize=[8,4], heatmap_names=['Image 1', 'Image 2'], slices='both')
    plt.suptitle(f'{file_name1.split(".")[0].replace("_", " ")} vs {file_name2.split(".")[0].replace("_", " ")}')
    plt.tight_layout()
    plt.show(block=True)

    pli.heatmap_slicer(np.arange(image1.shape[0]),np.arange(image1.shape[1]),
                    [image1 - np.rot90(image2,3)], figsize=[8,4], heatmap_names=['Image 1'], slices='both')
    plt.suptitle(f'{file_name1.split(".")[0].replace("_", " ")} - {file_name2.split(".")[0].replace("_", " ")}')
    plt.tight_layout()
    plt.show(block=True)
    # Plot mean over Y
    plt.figure()
    plt.title('Image (Averaged over Y)')
    plt.plot(np.mean(image1[:, 100:-100], axis=1))
    plt.plot(np.mean(np.rot90(image2,3)[:, 100:-100], axis=1))
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel Y')
    plt.legend(['Image 1', 'Image 2'])
    plt.show(block=True)
    # Plot mean over X
    plt.figure()
    plt.title('Image (Averaged over X)')
    plt.plot(np.mean(image1[:-250, :], axis=0))
    plt.plot(np.mean(np.rot90(image2,3)[:-250, :], axis=0))
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel X')
    plt.legend(['Image 1', 'Image 2'])
    plt.show(block=True)

def standard_scaler(image):
    return (image - np.mean(image)) / np.std(image)

# Get all GGEMS and GATE MHD files
ggems_files = sorted(glob.glob('out/*fastcat*.npy'))
gate_files = sorted(glob.glob('out/*ggems_1e09*p.mhd'))

print(ggems_files,gate_files)
# Check if the number of GGEMS and GATE files are the same
if len(ggems_files) != len(gate_files):
    print("The number of GGEMS and GATE files are not the same.")
    exit(1)

print(ggems_files,gate_files)
# Compare each pair of GGEMS and GATE images
for ggems_file, gate_file in zip(ggems_files, gate_files):
    print(f'Comparing {ggems_file} and {gate_file}...')
    ggems_image, gate_image = compare_images(ggems_file, gate_file)

    if args.vis == True:
        visualize_comparison(ggems_image, gate_image, ggems_file, gate_file)