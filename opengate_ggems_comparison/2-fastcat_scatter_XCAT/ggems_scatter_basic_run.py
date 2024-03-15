# Read the mhd file from data
from fastcat.ggems_scatter import generate_ggems_bash_script
import fastcat as fc
import numpy as np


# Read the mhd file from data
range_file = '/home/jericho/1-Workspace/fastcat_ggems/test/mhd_file_test_range.txt'
mhd_file = '/home/jericho/1-Workspace/fastcat_ggems/test/mhd_file_test.mhd'
material_file = '/home/jericho/1-Workspace/fastcat_ggems/custom_materials_gate.txt'
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'
nparticles = 3000000000
out = 'out'

s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)
spectrum = spectrum_file
s_max = s.x.max()

Catphan604_phantom = fc.utils.get_phantom_from_mhd(
    mhd_file, range_file, material_file)
angles = np.linspace(0, np.pi*2, 90)

generate_ggems_bash_script(Catphan604_phantom, angles=angles, spectrum=spectrum_file,
                           s_max=s_max, detector_material='CsI',
                           nparticles=nparticles,
                           output_dir='/home/jericho/1-Workspace/opengate_ggems_comparison/2-fastcat_scatter_XCAT/test/')

Catphan604_phantom.run_ggems_bash_script()
