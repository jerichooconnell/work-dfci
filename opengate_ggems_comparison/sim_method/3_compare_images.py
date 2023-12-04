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

parser.add_argument('-nv', '--novis', required=False, action='store_false', help='Visualize the comparison')
parser.add_argument('-s', '--specs', required=False, nargs='+', help='List of file specifications to compare')

args = parser.parse_args()

def process_image(image_path):
    # Read the image
    if image_path.endswith('.npy'):
        image = np.load(image_path)
        image = np.fliplr(image)
    else:
        itkimage = sitk.ReadImage(image_path)
        image = sitk.GetArrayFromImage(itkimage)
        # check if the word ggems is in the title of the file
        if 'ggems' in image_path:
            image = np.rot90(image, 3)

    # Normalize the image
    image = standard_scaler(image.squeeze())

    return image

def standard_scaler(image,edge=10):
    # If the array is 1D
    if edge == 0:
        return (image - np.mean(image)) / np.std(image)
    else:
        if len(image.shape) == 1:
            return (image - np.mean(image[edge:-edge])) / np.std(image[edge:-edge])
        else:
            return (image - np.nanmean(image[edge:-edge,edge:-edge])) / np.nanstd(image[edge:-edge,edge:-edge])

def visualize_comparison(images, file_names):
    # Assuming images is your list of normalized images
    # and they are numpy arrays
    
    # print(file_names)
    # Display heatmaps
    heatmap_slicer(np.arange(images[0].shape[0]),np.arange(images[0].shape[1]),
                    images, figsize=[10,6], heatmap_names=[file_name[:10] for file_name in file_names],
                     slices='both',vmin=np.percentile(images[0],0.5),vmax=np.percentile(images[0],99.5))
    plt.suptitle(' vs '.join(file_names))
    plt.tight_layout()
    plt.show(block=True)

    profs = []
    for image in images:
        profs.append(standard_scaler(np.mean(image[:, 100:-100], axis=1)))
    
    plt.figure()
    plt.title('Image (Averaged over Y)')
    for ii, prof in enumerate(profs):
        plt.plot(prof)
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel Y')
    # plt.legend(['Analytical', 'GGEMS','Gate'])
    plt.show(block=True)
    # Plot mean over X

    profs = []
    for image in images:
        profs.append(standard_scaler(np.mean(image[:-250, :], axis=0)))
    
    plt.figure()
    plt.title('Image (Averaged over X)')
    lw=1
    for ii, prof in enumerate(profs):
        plt.plot(prof,lw=lw)
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel X')
    # plt.legend(['Analytical', 'GGEMS','Gate'])
    plt.show(block=True)

# Check if running as a script
if __name__ == '__main__':

    # Check if the user specified a list of files to compare
    if args.specs != None:
        spec_list = args.specs
    else:
        spec_list = ['out/*ggems_1e09*p.mhd','out/*gate_5e08*[!_uncertainty].mhd']

    print(f'Lists of globs: {spec_list}')
    # def custom_sort(file):
    #     return '2' in file, file
    
    files = []
    # Get all GGEMS and GATE MHD files
    for specs in spec_list:
        files.append(sorted(glob.glob(specs)))

    # Process each image individually and append to list
    images = []
    file_names = []
    for ii, file in enumerate(files):
        images.append([])
        file_names.append([])
        for image_file in file:
            print(f'Processing {image_file}...')
            image = process_image(image_file)
            images[ii].append(image)
            file_names[ii].append(image_file.split('/')[-1].split('.')[0].replace('_', ' '))

    try:
        images = np.array(images)
        file_names = np.array(file_names)
    except:
        print('Images of different sizes, cannot compare')
        print(f'Image shapes: {[len(image) for image in images]}')
        exit(1)

    if args.novis == True:
        for jj in range(len(images[0])):
            visualize_comparison(images[:,jj,:,:], file_names[:,jj])

    # visualize_comparison(images, file_names)

# def visualize_comparison(image1, image2, image3, file_name1='GGEMS',file_name2='GATE'):

#     # Assuming image1 and image2 are your normalized images
#     # and they are numpy arrays

#     # Display heatmaps
#     heatmap_slicer(np.arange(image1.shape[0]),np.arange(image1.shape[1]),
#                     [image1, np.rot90(image2,3), np.rot90(image3,0)], figsize=[8,4], heatmap_names=['Analytical', 'GGEMS','Gate'],
#                      slices='both',vmin=np.percentile(image1,0.5),vmax=np.percentile(image1,99.5))
#     plt.suptitle(f'{file_name1.split(".")[0].replace("_", " ")} vs {file_name2.split(".")[0].replace("_", " ")}')
#     plt.tight_layout()
#     plt.show(block=True)

#     # pli.heatmap_slicer(np.arange(image1.shape[0]),np.arange(image1.shape[1]),
#     # #                 [image1 - np.rot90(image2,3)], figsize=[8,4], heatmap_names=['Image 1'], slices='both')
#     # plt.suptitle(f'{file_name1.split(".")[0].replace("_", " ")} - {file_name2.split(".")[0].replace("_", " ")}')
#     # plt.tight_layout()
#     # plt.show(block=True)
#     # Plot mean over Y
    
#     prof_1 = np.mean(image1[:, 100:-100], axis=1)
#     prof_2 = np.mean(np.rot90(image2,3)[:, 100:-100], axis=1)
#     prof_3 = np.mean(np.rot90(image3,0)[:, 100:-100], axis=1)

#     prof_1 = standard_scaler(prof_1)
#     prof_2 = standard_scaler(prof_2)
#     prof_3 = standard_scaler(prof_3)

#     plt.figure()
#     plt.title('Image (Averaged over Y)')
#     plt.plot(prof_1)
#     plt.plot(prof_2)
#     plt.plot(prof_3)
#     plt.ylabel('Relative Energy Deposition [a.u]')
#     plt.xlabel('Pixel Y')
#     plt.legend(['Analytical', 'GGEMS','Gate'])
#     plt.show(block=True)
#     # Plot mean over X

#     prof_1 = np.mean(image1[:-250, :], axis=0)
#     prof_2 = np.mean(np.rot90(image2,3)[:-250, :], axis=0)
#     prof_3 = np.mean(np.rot90(image3,0)[:-250, :], axis=0)

#     prof_1 = standard_scaler(prof_1)
#     prof_2 = standard_scaler(prof_2)
#     prof_3 = standard_scaler(prof_3)
#     plt.figure()
#     plt.title('Image (Averaged over X)')
#     lw=1
#     plt.plot(prof_1,lw=lw)
#     plt.plot(prof_2,lw=lw)
#     plt.plot(prof_3,lw=lw)
#     plt.ylabel('Relative Energy Deposition [a.u]')
#     plt.xlabel('Pixel X')
#     plt.legend(['Analytical', 'GGEMS','Gate'])
#     plt.show(block=True)


# # Get all GGEMS and GATE MHD files
# fastcat_files = sorted(glob.glob('out/*fastcat*.npy'))
# ggems_files = sorted(glob.glob('out/*ggems_1e09*p.mhd'))
# gate_files = sorted(glob.glob('out/*ogate_5e08*p.mhd'))

# print(ggems_files,gate_files)
# # Check if the number of GGEMS and GATE files are the same
# if len(ggems_files) != len(gate_files):
#     print("The number of GGEMS and GATE files are not the same.")
#     exit(1)

# print(ggems_files,gate_files)
# # Compare each pair of GGEMS and GATE images
# for fastcat_file, ggems_file, gate_file in zip(fastcat_files, ggems_files, gate_files):
#     print(f'Comparing {ggems_file} and {gate_file}...')
#     fastcat_image, ggems_image, gate_image = compare_images(fastcat_file, ggems_file, gate_file)

#     if args.vis == True:
#         visualize_comparison(fastcat_image, ggems_image, gate_image, ggems_file, gate_file)