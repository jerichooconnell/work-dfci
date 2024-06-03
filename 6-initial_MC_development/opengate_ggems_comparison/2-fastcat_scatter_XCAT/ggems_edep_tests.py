# %%
# Test the fastcat mhd file reader from fastcat.utils
import fastcat as fc
import argparse
import fastcat.ggems_scatter as gg_scatter

# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
  prog='image_viewer.py',
  description='''-->> 6 - OpenGL Visualization Example <<--''',
  epilog='''''',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-np', '--np', required=False,type=int, default=int(1e5), help='Number of particles')
parser.add_argument('-body', '--body', required=False, action='store_true', help='Include body in simulation')
parser.add_argument('-spect', '--spect', required=False, action='store_false', help='Include spectrum in simulation')
parser.add_argument('-edep', '--edep', required=False, action='store_false', help='Include edep in simulation')

args = parser.parse_args()

if args.body:
    range_file = '/home/jericho/1-Workspace/fastcat_ggems/test/mhd_file_test_range.txt'
else:
    range_file = '/home/jericho/1-Workspace/fastcat_ggems/test/mhd_file_test_range.txt'

# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_ggems/test/mhd_file_test.mhd'
material_file = '/home/jericho/1-Workspace/fastcat_ggems/custom_materials_gate.txt'
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'
 
nparticles = float(args.np)
out = 'out'

if args.spect:  
    print('Loading spectrum')
    s = fc.Spectrum()
    s.load(spectrum_file=spectrum_file) 
    spectrum = spectrum_file
    s_max= s.x.max()
else:
    spectrum = None
    s_max = None

Catphan604_phantom, spectrum = fc.utils.init_ggems_scatter_simulation(mhd_file=mhd_file,range_file=range_file,
                                                                      material_file=material_file,
                                                                      spectrum_file=spectrum_file)

# import matplotlib.pyplot as plt
# plt.figure()
# import mpl_interactions as pli
# pli.hyperslicer(Catphan604_phantom.phantom, axis=0, cmap='jet')
# plt.show(block=True)
print(Catphan604_phantom.mhd_file)
# %%
if args.body:
    output_file = 'no_body_'
else:
    output_file = ''

gg_scatter.run_ggems_scatter_simulation(Catphan604_phantom,
                                    nparticles=int(nparticles),
                                    output_file=output_file,
                                    output_dir=out,
                                    spectrum=spectrum_file,
                                    detector_material='CsI',
                                    vis=False,
                                    edep_detector=args.edep,s_max=s_max)