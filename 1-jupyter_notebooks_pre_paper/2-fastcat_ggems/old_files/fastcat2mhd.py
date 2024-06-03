# Convert a fastcat simulation to a mhd format

import sys
import numpy as np
import SimpleITK as sitk
import fastcat as fc


s = fc.Spectrum()
nviews = 2

phantom = fc.XCAT2()
s.load('C_spectrum_25')
kernel = fc.Kernel(s, 'CsI-784-micrometer')
angles = np.linspace(0,np.pi/2,nviews)
phantom.return_projs(kernel,s,angles,det_on=True,scat_on=False,mgy=7/nviews)

