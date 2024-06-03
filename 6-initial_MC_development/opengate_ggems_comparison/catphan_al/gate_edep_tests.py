# Test the fastcat mhd file reader from fastcat.utils
import fastcat as fc
import fastcat.ogate_scatter as og_scatter
import argparse

# ------------------------------------------------------------------------------
# Read arguments
parser = argparse.ArgumentParser(
  prog='image_viewer.py',
  description='''-->> 6 - OpenGL Visualization Example <<--''',
  epilog='''''',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-np', '--np', required=False,type=int, default=int(1e5), help='Number of particles')
parser.add_argument('-nt', '--nt', required=False, type=int, default=15, help='Number of threads')
parser.add_argument('-body', '--body', required=False, action='store_true', help='Include body in simulation')
parser.add_argument('-spect', '--spect', required=False, action='store_true', help='Include spectrum in simulation')

args = parser.parse_args()

if args.body:
    range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
else:
    range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range_no_phantom_body.txt'

# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.db'
material_file1 = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'

# import mpl_interactions as pli
s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)      
nparticles = float(args.np)
out = 'out'
if args.spect:
    spectrum = s
else:
    spectrum = None

Catphan604_phantom = fc.utils.get_phantom_from_mhd(mhd_file,range_file,material_file1)

if args.body:
    output_file = 'no_body_'
else:
    output_file = ''

og_scatter.run_ogate_scatter_simulation(Catphan604_phantom,
                                    nparticles=nparticles,
                                    output_file=output_file,
                                    output_dir=out,
                                    material_file= material_file,
                                    detector_material='CsI',
                                    spectrum=spectrum,
                                    vis=False,
                                    nt=args.nt)