get_ipython().run_line_magic('pylab', 'nbagg')

import mpl_interactions as pli
from read_in_data import load_itk
import numpy as np
import matplotlib.pyplot as plt

ggems_image, origin, space = load_itk('out/ggems_dosimetry_edep.mhd') # What is this in? - Should be MeV as well according to didier
ogate_image, origin, space = load_itk('out/gate_edep_test.mhd') # This is in MeV, MeV per particle? - I don't bel

fig = plt.figure()
plt.subplot(121)
crop = 75

a = c = crop
b = d = -crop
log_ggems = np.log(np.flipud(ggems_image.transpose(2,1,0))[:,a:b,c:d]+1)
log_gate = np.log(ogate_image[:,a:b,c:d]+1)

ggems = np.flipud(ggems_image.transpose(2,1,0))[:,a:b,c:d]
ogate = ogate_image[:,a:b,c:d]

controls = pli.hyperslicer(log_ggems,cmap='jet',title='GGEMS z= {axis0:.2f} [0.1 mm]')
plt.axis('off')
plt.subplot(122)
pli.hyperslicer(log_gate,controls=controls,cmap='jet',title='Gate z= {axis0:.2f} [0.1 mm]')
plt.axis('off')
plt.show()
