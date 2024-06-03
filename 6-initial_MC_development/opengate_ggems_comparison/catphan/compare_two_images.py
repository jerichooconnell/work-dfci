import matplotlib.pyplot as plt 
import numpy as np
# from read_in_data import load_itk
import mpl_interactions as pli
import SimpleITK as sitk
import argparse

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

parser.add_argument('image', default='out/run_1e10.mhd', help='first image')
parser.add_argument('image2', default='out/run_1e10.mhd', help='second image')
parser.add_argument('-n','--norm', action='store_true', help='normalize images')
parser.add_argument('-m','--mean', action='store_true', help='plot_means')

args = parser.parse_args()

ggems_image, origin, space = load_itk(args.image) # What is this in? - Should be MeV as well according to didier
ggems_image2, origin, space = load_itk(args.image2) # What is this in? - Should be MeV as well according to didier

ggems_image = ggems_image[10:-10,10:-10]
ggems_image2 = ggems_image2[10:-10,10:-10]

if bool(args.norm):
    ggems_image = (ggems_image - np.mean(ggems_image))/np.std(ggems_image)
    ggems_image2 = (ggems_image2 - np.mean(ggems_image2))/np.std(ggems_image2)

pli.heatmap_slicer(range(ggems_image.shape[0]),range(ggems_image.shape[1]),
                   [ggems_image,ggems_image2],figsize=[12,4],slices='both')

plt.tight_layout()

plt.show(block=True)

if bool(args.mean):
    plt.figure()
    plt.title('100keV Catphan Image (Averaged over Y)')
    plt.plot(np.mean(ggems_image,axis=1))
    plt.plot(np.mean(ggems_image2,axis=1))
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel Y')
    plt.show(block=True)

    plt.figure()
    plt.title('100keV Catphan Image (Averaged over X)')
    plt.plot(np.mean(ggems_image,axis=0))
    plt.plot(np.mean(ggems_image2,axis=0))
    plt.ylabel('Relative Energy Deposition [a.u]')
    plt.xlabel('Pixel X')
    plt.show(block=True)