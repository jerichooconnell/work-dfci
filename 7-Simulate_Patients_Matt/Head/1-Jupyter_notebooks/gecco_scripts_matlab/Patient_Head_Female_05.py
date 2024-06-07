
import numpy as np
from gecco import patient_data, calculate_spectrum_sp
from gecco.utils import nrrd_to_mhd
from scipy.io import savemat
import os

phantom = patient_data.patient_phantom('/home/berbecolab/2-Datadir/Clinical_data/Head/Patient_Head_Female_05.nrrd', 1e10, reload=True, sim_num=None)

# Source spectrum
spectrum = calculate_spectrum_sp(140,12)

# Beam filters
spectrum.filter('Be', 1.5)
spectrum.filter('Al', 2.75)
spectrum.filter('Ti', 0.89)

# Detector filters
spectrum.filter('Al', 3.7)
spectrum.filter('C', 3.8*(2/1.7)) # Difference in density

phantom.xx, phantom.yy = spectrum.get_points()
phantom.run_gecco(1e20,360,conv_on=False)

phantom.correct_intensity(ml=False,crop=40)
phantom.interpolate_ggems_scatter()
phantom.calc_gecco_projections(scat_weight=0.48,noise_weight=100) # Creates the gecco projections scatter to primary reduction from asg is 0.48 assumed half is taken by scatter correction

# --------------------- Second Layer ----------------

phantom2 = patient_data.patient_phantom('/home/berbecolab/2-Datadir/Clinical_data/Head/Patient_Head_Female_05.nrrd', 1e10, reload=True, sim_num=None, second_layer=True)

# Source spectrum
spectrum = calculate_spectrum_sp(140,12)

# Beam filters
spectrum.filter('Be', 1.5)
spectrum.filter('Al', 2.75)
spectrum.filter('Ti', 0.89)

# Detector filters
spectrum.filter('Al', 3.7)
spectrum.filter('C', 3.8*(2/1.7)) # Difference in density

# First layer filters
spectrum.filter('Cesium Iodide',0.6*0.71) # 71% fill factor
spectrum.filter('Si',1.1)

phantom2.run_gecco(1e20,360,conv_on=False)

phantom2.correct_intensity(ml=False,crop=40)
phantom2.interpolate_ggems_scatter()
phantom2.calc_gecco_projections(scat_weight=0.48,noise_weight=100)

nrrd_base = 'Patient_Head_Female_05'

out = '/home/berbecolab/1-Workspace/1-Workspace/7-Simulate_Patients_Matt/Head/1-Jupyter_notebooks/gecco_data_matlab'

if not os.path.exists(os.path.join(out,nrrd_base)):
    os.makedirs(os.path.join(out,nrrd_base))

savemat(os.path.join(out,nrrd_base, nrrd_base + '_scatter_first_layer' + '.mat'),
        { "Patient_Head_Female_05": phantom.ggems_scatter_denoised })
savemat(os.path.join(out,nrrd_base, nrrd_base + '_scatter_second_layer'+ '.mat'),
        { "Patient_Head_Female_05": phantom2.ggems_scatter_denoised })

savemat(os.path.join(out,nrrd_base, nrrd_base + '_primary_first_layer'+ '.mat'),
        { "Patient_Head_Female_05": phantom.primary_projections })
savemat(os.path.join(out,nrrd_base, nrrd_base + '_primary_second_layer'+ '.mat'),
        { "Patient_Head_Female_05": phantom2.primary_projections })

savemat(os.path.join(out,nrrd_base, nrrd_base + '_flood_first_layer'+ '.mat'),
        { "Patient_Head_Female_05": phantom.flood_field })
savemat(os.path.join(out,nrrd_base, nrrd_base + '_flood_second_layer'+ '.mat'),
        { "Patient_Head_Female_05": phantom2.flood_field })

with open(os.path.join(out, nrrd_base, nrrd_base + "_simulation_info.txt"), 'w') as f:
            f.write(str(phantom))

