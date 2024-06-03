import SimpleITK as sitk
import numpy as np
import glob
import matplotlib.pyplot as plt
from mpl_interactions import heatmap_slicer

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

def compare_images(image1_path, image2_path, image3_path):
    # Read the images
    # Reads the image using SimpleITK
    # itkimage1 = sitk.ReadImage(image1_path)

    image1 = np.load(image1_path)
    image1 = np.fliplr(image1)

    itkimage2 = sitk.ReadImage(image2_path)
    itkimage3 = sitk.ReadImage(image3_path)


    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    image3 = sitk.GetArrayFromImage(itkimage3)
    image2 = sitk.GetArrayFromImage(itkimage2)

    # Normalize the images
    image1 = standard_scaler(image1.squeeze())
    image2 = standard_scaler(image2.squeeze())
    image3 = standard_scaler(image3.squeeze())

    # Calculate and print the statistics for image 1 and 2
    difference = image1 - image2
    mean_difference = np.mean(difference)
    std_difference = np.std(difference)
    
    print(f'Analytical vs gate mean difference: {mean_difference}')
    print(f'Analytical vs gate standard deviation of difference: {std_difference}')

    # Calculate and print the statistics for image 1 and 3
    difference = image1 - image3
    mean_difference = np.mean(difference)
    std_difference = np.std(difference)

    print(f'Analytical vs ggems mean difference: {mean_difference}')
    print(f'Analytical vs ggems standard deviation of difference: {std_difference}')


    return image1.squeeze(), image2.squeeze(), image3.squeeze()

def visualize_comparison(image1, image2, image3, file_name1='GGEMS',file_name2='GATE'):

    # Assuming image1 and image2 are your normalized images
    # and they are numpy arrays

    # Display heatmaps
    heatmap_slicer(np.arange(image1.shape[0]),np.arange(image1.shape[1]),
                    [image1, np.rot90(image2,3), np.rot90(image3,0)], figsize=[8,4], heatmap_names=['Analytical', 'GGEMS','Gate'],
                     slices='both',vmin=np.percentile(image1,0.5),vmax=np.percentile(image1,99.5))
    plt.suptitle(f'{file_name1.split(".")[0].replace("_", " ")} vs {file_name2.split(".")[0].replace("_", " ")}')
    plt.tight_layout()
    plt.show(block=True)

    # pli.heatmap_slicer(np.arange(image1.shape[0]),np.arange(image1.shape[1]),
    # #                 [image1 - np.rot90(image2,3)], figsize=[8,4], heatmap_names=['Image 1'], slices='both')
    # plt.suptitle(f'{file_name1.split(".")[0].replace("_", " ")} - {file_name2.split(".")[0].replace("_", " ")}')
    # plt.tight_layout()
    # plt.show(block=True)
    # Plot mean over Y
    
    prof_1 = np.mean(image1[:, 100:-100], axis=1)
    prof_2 = np.mean(np.rot90(image2,3)[:, 100:-100], axis=1)
    prof_3 = np.mean(np.rot90(image3,0)[:, 100:-100], axis=1)

    prof_1 = standard_scaler(prof_1)
    prof_2 = standard_scaler(prof_2)
    prof_3 = standard_scaler(prof_3)

    plt.figure()
    plt.title('Image (Averaged over Y)')
    plt.plot(prof_1)
    plt.plot(prof_2)
    plt.plot(prof_3)
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel Y')
    plt.legend(['Analytical', 'GGEMS','Gate'])
    plt.show(block=True)
    # Plot mean over X

    prof_1 = np.mean(image1[:-250, :], axis=0)
    prof_2 = np.mean(np.rot90(image2,3)[:-250, :], axis=0)
    prof_3 = np.mean(np.rot90(image3,0)[:-250, :], axis=0)

    prof_1 = standard_scaler(prof_1)
    prof_2 = standard_scaler(prof_2)
    prof_3 = standard_scaler(prof_3)
    plt.figure()
    plt.title('Image (Averaged over X)')
    lw=1
    plt.plot(prof_1,lw=lw)
    plt.plot(prof_2,lw=lw)
    plt.plot(prof_3,lw=lw)
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel X')
    plt.legend(['Analytical', 'GGEMS','Gate'])
    plt.show(block=True)

def standard_scaler(image,edge=10):
    # If the array is 1D
    if edge == 0:
        return (image - np.mean(image)) / np.std(image)
    else:
        if len(image.shape) == 1:
            return (image - np.mean(image[edge:-edge])) / np.std(image[edge:-edge])
        else:
            return (image - np.nanmean(image[edge:-edge,edge:-edge])) / np.nanstd(image[edge:-edge,edge:-edge])

# Get all GGEMS and GATE MHD files
fastcat_files = sorted(glob.glob('out/*fastcat*.npy'))
ggems_files = sorted(glob.glob('out/*ggems_1e09*p.mhd'))
gate_files = sorted(glob.glob('out/*ogate_5e08*p.mhd'))

print(ggems_files,gate_files)
# Check if the number of GGEMS and GATE files are the same
if len(ggems_files) != len(gate_files):
    print("The number of GGEMS and GATE files are not the same.")
    exit(1)

print(ggems_files,gate_files)
# Compare each pair of GGEMS and GATE images
for fastcat_file, ggems_file, gate_file in zip(fastcat_files, ggems_files, gate_files):
    print(f'Comparing {ggems_file} and {gate_file}...')
    fastcat_image, ggems_image, gate_image = compare_images(fastcat_file, ggems_file, gate_file)

    if args.vis == True:
        visualize_comparison(fastcat_image, ggems_image, gate_image, ggems_file, gate_file)