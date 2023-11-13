# Test the fastcat mhd file reader from fastcat.utils
import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt
import fastcat.ggems_scatter as gg_scatter


# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range_no_phantom_body.txt'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'

Catphan604_phantom = fc.utils.get_phantom_from_mhd(mhd_file,range_file,material_file)
# import mpl_interactions as pli
s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)
det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,180,endpoint=False)
np=int(1e8)        
out = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/out'
edep_detector = False
edep = 'edep' if edep_detector else 'counts'
file_name = f'{out}/ggems_{f"{np:.0e}".replace("+", "")}_{s.x.max():.0f}kVp_{edep}_no_body'


gg_scatter.run_ggems_scatter_simulation(Catphan604_phantom,
                                        nparticles=np,
                                        output_file=file_name,
                                        spectrum=spectrum_file,
                                        detector_material='CsI',
                                        vis=False,
                                        edep_detector=edep_detector)

# Make an output file name that includes the number of particles in scientific notation, the max spectrum energy, 
# and the detector material, whether it is edep or not

