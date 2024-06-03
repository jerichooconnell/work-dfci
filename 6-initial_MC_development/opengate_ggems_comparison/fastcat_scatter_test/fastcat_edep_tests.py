# %%
# Test the fastcat mhd file reader from fastcat.utils
import numpy as np
import fastcat as fc
import pickle 
#%%
pickle_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/fastcat_scatter_test/test/ggems_1e03_121kVp.pkl'

# Load the fastcat simulation from the pickle file
with open(pickle_file, 'rb') as f:
    phantom = pickle.load(f)
    print('Done loading simulation parameters from ' + pickle_file)

# Get the simulation parameters
simulation_parameters = phantom.simulation_parameters
detector_material = simulation_parameters['detector_material']
spectrum = simulation_parameters['spectrum']

# Load the spectrum as a fastcat spectrum object
s = fc.Spectrum()
s.load(spectrum_file=spectrum)

det = fc.Detector(s,'CsI-784-micrometer')
angles = np.linspace(0,np.pi*2,2,endpoint=False) 

# return the projections
phantom.return_projs(det,s,angles,mgy=0, 
                    ASG=False, scat_on=False,
                    det_on=False,
                    filter_on=False,
                    return_intensity=True)

# kv_max = spectrum.x.max()

# %%
# Read in the first mhd file from the ggems_scatter simulation
mhd_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/fastcat_scatter_test/test/out/ggems_1e07_121kVp_0000.mhd'
mhd_scatter_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/fastcat_scatter_test/test/out/ggems_1e07_121kVp_0000-scatter.mhd'

fc_projection = phantom.intensity[0]

image1_path = '/home/jericho/1-Workspace/opengate_ggems_comparison/catphan/out/ggems_1e09_121kVp_edepTrue_edep.mhd'
fc_projection = fc.utils.read_mhd(mhd_file)

# ggems_primary = np.fliplr(image1)
# Read the mhd file from data
ggems_projection = fc.utils.read_mhd(mhd_file)
ggems_projection_scatter = fc.utils.read_mhd(mhd_scatter_file)

ggems_primary = ggems_projection - ggems_projection_scatter

# Crop the ggems and fastcat projection
edge = 1
ggems_primary = ggems_primary[:-edge,:]
fc_projection = fc_projection[:-edge,:]

# define the standard scaler function
def standard_scaler_ref(x, edge):
    return (x - x[edge:-edge,edge:-edge].mean()) / x[edge:-edge,edge:-edge].std(), x[edge:-edge,edge:-edge].mean(), x[edge:-edge,edge:-edge].std()

def rescale(x_new, mean, std, edge=10):
    # x_new = (x - x[edge:-edge,edge:-edge].mean()) / x[edge:-edge,edge:-edge].std()
    return x_new * std + mean


fc_projection, fc_mean, fc_std = standard_scaler_ref(fc_projection,edge=30)
ggems_rescale, ggems_mean, ggems_std = standard_scaler_ref(ggems_primary,edge=30)

phantom.fc_parameters = {}
phantom.fc_parameters['fc_mean'] = fc_mean
phantom.fc_parameters['fc_std'] = fc_std
phantom.fc_parameters['ggems_mean'] = ggems_mean
phantom.fc_parameters['ggems_std'] = ggems_std

# Rescale the fastcat projection to match the ggems projection
# fc_projection = rescale(fc_projection, ggems_mean, ggems_std)

# Make a plot of the fc_projection and the ggems_primary projection
import matplotlib.pyplot as plt
plt.figure()
plt.plot(np.mean(fc_projection,axis=0))
plt.plot(np.mean(ggems_rescale,axis=0))
plt.show(block=True)
# %%
