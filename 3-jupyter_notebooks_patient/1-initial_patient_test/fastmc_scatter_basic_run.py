# Read the mhd file from data
import os
from fastcat.ggems_scatter import generate_ggems_bash_script
import fastcat as fc
import numpy as np
from fastcat.patient_data import patient_phantom
from fastcat.fastmc_scatter import write_fastmc_xml_file, run_fastmc_files, write_fastmc_flood_field_xml_file

out_file = '/home/jericho/1-Workspace/1-jupyter_notebooks/2-fastcat_ggems/test'
spectrum_file = '/home/jericho/1-Workspace/1-jupyter_notebooks/4-preliminary_fastmc_projections/spectrum_120kVp_2.75mmAl_0.89mmTi.dat'

# nparticles = 1000000  # 000
out = 'out'

s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)
s_max = s.x.max()

phantom = patient_phantom('brain', 1e10, is_fullfan=True)
phantom.spectrum_file = spectrum_file
angles = np.linspace(0, np.pi*2, 10, endpoint=False)

file_base = 'test'
phantom.sim_angles = angles
out_dir = 'out_dir'
sim_dir = 'sim_dir'


this_dir = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(this_dir, out_dir)
sim_dir = os.path.join(this_dir, sim_dir)
file_base = os.path.join(this_dir, file_base)

write_fastmc_flood_field_xml_file(phantom=phantom, out_dir=out_dir, sim_dir=sim_dir,
                                  file_name=file_base, half_fan=False)

write_fastmc_xml_file(phantom=phantom, out_dir=out_dir, sim_dir=sim_dir,
                      file_name=file_base, half_fan=False)

run_fastmc_files(
    lib_path='/home/jericho/Downloads/FastMC_Jan_05/FastMC_install/bin/FastMC', sim_dir=sim_dir)
