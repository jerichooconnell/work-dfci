
import numpy as np
from gecco import patient_data, calculate_spectrum_sp
from gecco.utils import nrrd_to_mhd

nrrd_file = '/media/jericho/T7/Clinical_data/Pelvis/Pelvis_Female_Patient_3.nrrd'

# Write to mhd

nrrd_to_mhd(nrrd_file,force=True,tr= [1, 0, 2],crop=[287, 511, 2, 392, 15, 78])

phantom = patient_data.patient_phantom(nrrd_file, 10000000000.0, force_materials=False, is_fullfan=False)

# Pixel size
phantom.geomet.nDetector = np.array([360,360])
phantom.geomet.dDetector = np.array([1.12,1.12])
phantom.geomet.sDetector = phantom.geomet.dDetector*phantom.geomet.nDetector

# Spectrum
spectrum = calculate_spectrum_sp(140,12)
spectrum.filter('Al', 2.75)
spectrum.filter('Be', 1.5)
spectrum.filter('Ti', 0.89)

phantom.initialize_fastmc(10,spectrum)

phantom.run_fastmc(fastmc_path ='/home/jericho/Downloads/FastMC_Jan_05/FastMC_install/bin/FastMC')

phantom.load_ggems()

print()
print('Done - Completed without errors')
