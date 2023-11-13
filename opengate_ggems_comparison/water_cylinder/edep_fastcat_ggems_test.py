# Test the fastcat mhd file reader from fastcat.utils
import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt
import fastcat.ggems_scatter as gg_scatter


# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'

Catphan604_phantom = fc.utils.get_phantom_from_mhd(mhd_file,range_file,material_file)
# import mpl_interactions as pli
s = fc.spectrum.Spekpy(120,12)

# Make a dummy spectrum
s.x = np.array([99.999, 100, 100.001])
s.y = np.array([0,1,0])
# s.attenuate(0.4,fc.get_mu(z=13))
det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,180,endpoint=False)        

out = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/run_edep_1e10'

gg_scatter.run_ggems_scatter_simulation(Catphan604_phantom,
                                        nparticles=int(1e10),
                                        output_file=out,
                                        detector_material='CsI',
                                        vis=False,edep_detector=True)
