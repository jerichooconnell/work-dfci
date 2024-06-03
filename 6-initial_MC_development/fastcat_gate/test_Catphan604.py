import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt


# Read the mhd file from data
mhd_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604.mhd'
range_file = '/home/jericho/1-Workspace/fastcat_gate/Catphan604_Range.txt'
material_file = '/home/jericho/1-Workspace/fastcat_gate/Materials.txt'

Catphan604_phantom = fc.utils.get_phantom_from_mhd(mhd_file,range_file,material_file)
import mpl_interactions as pli
s = fc.spectrum.Spekpy(120,12)
s.attenuate(0.4,fc.get_mu(z=13))
det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,180,endpoint=False)        

# print(Catphan604_phantom.geomet)
Catphan604_phantom.return_projs(det,s,angles, 
                                mgy=8, ASG=True,scat_on=False,
                                det_on=False,bowtie=True,
                                filter='bowtie_real')