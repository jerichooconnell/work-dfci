# Read the mhd file from data
from fastcat.ggems_scatter import generate_ggems_bash_script
import fastcat as fc
import numpy as np

out_file = '/home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test'
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'
range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
bowtie_file = '/home/jericho/Software/ct_scanner_example/data/full_fan.dat'

nparticles = 1000000000
out = 'out'

s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)
spectrum = spectrum_file
s_max = s.x.max()

Catphan604_phantom = fc.utils.get_phantom_from_mhd(
    mhd_file, range_file, material_file)
angles = np.linspace(0, np.pi*2, 2)

generate_ggems_bash_script(Catphan604_phantom, angles=angles, spectrum=spectrum_file,
                           s_max=s_max, detector_material='CsI',
                           nparticles=nparticles, bowtie_file=bowtie_file,
                           output_dir=out_file)

Catphan604_phantom.run_ggems_bash_script()
