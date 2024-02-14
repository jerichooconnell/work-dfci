# Read the mhd file from data
import fastcat as fc
import numpy as np
from fastcat.fastmc_scatter import write_fastmc_xml_file, run_fastmc_files, write_fastmc_flood_field_xml_file

out_file = '/home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test'

# 1024 * 768 is the real resolution of the detector

mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'
# spectrum_file = '/home/jericho/1-Workspace/1-jupyter_notebooks/4-preliminary_fastmc_projections/spectrum_120kVp_2.75mmAl_0.89mmTi.dat'
spectrum_file = '/home/jericho/Downloads/FastMC_Jan_05/FastMC_install/bin/data/80kV_3mmAl.dat'
range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
bowtie_file = '/home/jericho/Software/Catphan604_HeadSized/full_fan_1_deg_dummy.dat'

out = 'out'

s = fc.spectrum.Spekpy(80, 14)
s.attenuate(0.3, fc.get_mu('14'))  # As per varian

s.write_dat_file(spectrum_file)

spectrum = spectrum_file
s_max = s.x.max()

Catphan604_phantom = fc.utils.get_phantom_from_mhd(
    mhd_file, range_file, material_file)

Catphan604_phantom.detector_thickness = 0.8
Catphan604_phantom.detector_thickness2 = 0.6
Catphan604_phantom.detector_material = 'CsI'
Catphan604_phantom.nparticles_per_angle = int(1e10)
Catphan604_phantom.bowtie_file = bowtie_file
Catphan604_phantom.spectrum_file = spectrum_file
Catphan604_phantom.material_file = material_file
Catphan604_phantom.mhd_file = mhd_file
Catphan604_phantom.range_file = range_file

file_base = '/home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test/fastmc'
angles = np.linspace(0, np.pi*2, 2, endpoint=False)
fnames = []

Catphan604_phantom.angles = angles
out_dir = '/home/jericho/1-Workspace/1-jupyter_notebooks/6-fastmc_no_bowtie/out_fastmc'
sim_dir = '/home/jericho/1-Workspace/1-jupyter_notebooks/6-fastmc_no_bowtie/sim_fastmc'

write_fastmc_flood_field_xml_file(phantom=Catphan604_phantom, out_dir=out_dir, sim_dir=sim_dir,
                                  file_name=file_base, half_fan=False)

# write_fastmc_xml_file(phantom=Catphan604_phantom, out_dir=out_dir, sim_dir=sim_dir,
#                       file_name=file_base, half_fan=False)

# run_fastmc_files(
#     lib_path='/home/jericho/Downloads/FastMC_Jan_05/FastMC_install/bin/FastMC', sim_dir=sim_dir)