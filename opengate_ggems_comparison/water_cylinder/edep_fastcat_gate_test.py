# Test the fastcat mhd file reader from fastcat.utils
import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt
import fastcat.ogate_scatter as og_scatter


# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.db'
material_file1 = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'
Catphan604_phantom = fc.utils.get_phantom_from_mhd(mhd_file,range_file,material_file1)
spectrum_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/data/spectrum_120kVp_2mmAl.dat'

# import mpl_interactions as pli
s = fc.Spectrum()

# Make a dummy spectrum
# s.x = np.array([99.999, 100, 100.001])
# s.y = np.array([0,1,0])
# s.attenuate(0.4,fc.get_mu(z=13))
# s = fc.Spectrum()
s.load(spectrum_file=spectrum_file)

det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,180,endpoint=False)        
nparticles = 1e9
out = f'/home/jericho/1-Workspace/opengate_ggems_comparison/water_cylinder/out/gate_{str(nparticles)}_edep'

og_scatter.run_ogate_scatter_simulation(Catphan604_phantom,
                                        nparticles=nparticles,
                                        output_file=out,
                                        material_file= material_file,
                                        detector_material='CsI',
                                        spectrum=s,
                                        vis=False,
                                        nt=15)