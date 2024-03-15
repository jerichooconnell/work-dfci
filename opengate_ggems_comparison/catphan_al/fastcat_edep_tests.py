# Test the fastcat mhd file reader from fastcat.utils
import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

# Read arguments
parser = argparse.ArgumentParser(
  prog='image_viewer.py',
  description='''-->> 6 - OpenGL Visualization Example <<--''',
  epilog='''''',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-al', '--alum', required=False, action='store_false', help='Include body in simulation')
parser.add_argument('-s', '--spect', required=False, action='store_true', help='Include spectrum in simulation')
parser.add_argument('-p', '--prefix', required=False, type=str, default='', help='Prefix for output file')

args = parser.parse_args()

if args.alum:
    range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
else:
    range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range_Al_Cu.txt'
# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'

Catphan604_phantom = fc.utils.get_phantom_from_mhd(mhd_file,range_file,material_file)


# import mpl_interactions as pli
s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)
det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,10,endpoint=False)       

s2 = fc.Spectrum()
s2.x = np.array([99.99,100,100.01])
s2.y = np.array([0,1,0])

# import mpl_interactions as pli
s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)      
# nparticles = float(args.np)
out = 'out'

if args.spect:
    spectrum = s
else:
    spectrum = s2

if args.alum:
    output_file = args.prefix + 'no_al_'
else:
    output_file = args.prefix + ''

det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,2,endpoint=False) 

Catphan604_phantom.return_projs(det,spectrum,angles, 
                                mgy=0, ASG=False,scat_on=False,
                                det_on=False,
                                filter_on=False,
                                return_intensity=True)

image = Catphan604_phantom.intensity[0]

kv_max = spectrum.x.max()

np.save(os.path.join(out,f'{output_file}fastcat_{kv_max:.0f}kVp.npy'),image)
print(f'Saved image to {os.path.join(out,f"{output_file}fastcat_{kv_max:.0f}kVp.npy")}')