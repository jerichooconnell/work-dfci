import glob
import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt
import mpl_interactions as pli
from mpl_interactions import ipyplot as iplt
# Zoom the ggems projections
from scipy.ndimage import zoom
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

ggems_scatter_files = glob.glob(
    '/home/jericho/1-Workspace/opengate_ggems_comparison/2-fastcat_scatter_XCAT/test/out/ggems_3e09_121kVp_*scatter.mhd'
)
ggems_primary_files = glob.glob(
    '/home/jericho/1-Workspace/opengate_ggems_comparison/2-fastcat_scatter_XCAT/test/out/ggems_3e09_121kVp_*[!scatter].mhd'
)
pkl_file = '/home/jericho/1-Workspace/opengate_ggems_comparison/2-fastcat_scatter_XCAT/test/ggems_1e03_121kVp.pkl'

ggems_scatter_files.sort()
ggems_primary_files.sort()
ggems_primary_projections = []
ggems_scatter_projections = []

for ggems_scatter_file, ggems_primary_file in zip(ggems_scatter_files, ggems_primary_files):
    ggems_primary, b, c = fc.utils.read_mhd(ggems_primary_file)
    ggems_scatter, b, c = fc.utils.read_mhd(ggems_scatter_file)

    ggems_primary_projections.append(ggems_primary.squeeze())
    ggems_scatter_projections.append(ggems_scatter.squeeze())

# Load the pickled phantom
phantom = np.load(pkl_file, allow_pickle=True)

# Convert the phantom angles to degrees
phantom_angles = phantom.angles * 180 / np.pi

# Define the denoising functions


def downsize_block(image, block_size):
    image_size = image.shape[0]
    block_size = int(block_size)
    downsize = image_size//block_size
    image = image[:downsize*block_size, :downsize*block_size]
    image = image.reshape(downsize, block_size, downsize,
                          block_size).mean(axis=(1, 3))
    return image


def denoise_projections(projections):
    projections_zoomed = []

    for projection in projections:
        projection_zoomed_downsized = downsize_block(projection, 64)
        projection_zoomed = zoom(
            projection_zoomed_downsized, 64, order=4, mode='nearest')
        # Adjust the mean of the zoomed image to match the original
        projection_zoomed = projection_zoomed * \
            np.mean(projection) / np.mean(projection_zoomed)
        projections_zoomed.append(projection_zoomed)

    return projections_zoomed


# zoom the scatter projections using the zoom fromfunction
ggems_scatter_denoised = denoise_projections(ggems_scatter_projections)

# Get the simulation parameters
simulation_parameters = phantom.simulation_parameters
detector_material = simulation_parameters['detector_material']
spectrum = simulation_parameters['spectrum']

# Load the spectrum as a fastcat spectrum object
s = fc.Spectrum()
s.load(spectrum_file=spectrum)

det = fc.Detector(s, 'CsI-784-micrometer')
angles = phantom.angles

# return the projections
phantom.return_projs(det, s, angles, mgy=0,
                     ASG=False, scat_on=False,
                     det_on=False,
                     filter_on=False,
                     return_intensity=True)  # Get primary fastcat projections


ggems_primary_only = np.array(
    ggems_primary_projections) - np.array(ggems_scatter_projections)
# Set the mean and standard deviation of the ggems primary only projections to match the fastcat projections


def normalize_mean_and_std(array1, array2):
    array1 = array1 - np.mean(array1)
    array1 = array1 * np.std(array2) / np.std(array1)
    array1 = array1 + np.mean(array2)
    return array1


phantom_projections = normalize_mean_and_std(
    phantom.intensity, ggems_primary_only)


# %%

# Set up a shallow neural network to map the fastcat projections to the ggems_primary_only projections using sklearn

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    phantom.intensity[0].flatten(), ggems_primary_only[0].flatten(), test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
scaler.fit(X_train.reshape(-1, 1))
X_train_scaled = scaler.transform(X_train.reshape(-1, 1))
X_test_scaled = scaler.transform(X_test.reshape(-1, 1))

# Define the neural network
mlp = MLPRegressor(hidden_layer_sizes=(10, 10, 10),
                   activation='relu',
                   solver='adam',
                   max_iter=1000,
                   verbose=True,
                   random_state=42)

# Train the neural network
mlp.fit(X_train_scaled, y_train)

# Predict the test data
predictions = mlp.predict(X_test_scaled)

# # Plot the predictions vs the actual data
# plt.figure()
# plt.scatter(y_test, predictions)
# plt.xlabel('True Values')
# plt.ylabel('Predictions')

# # Plot the residuals
# plt.figure()
# plt.scatter(y_test, y_test - predictions)
# plt.xlabel('True Values')
# plt.ylabel('Residuals')

# Calculate the mean squared error
print('Mean squared error: ', mean_squared_error(y_test, predictions))

# %%
# Use the neural network to predict the ggems primary only projections from the fastcat projections
ggems_primary_only_nn = []
for projection in phantom.intensity:
    projection_scaled = scaler.transform(projection.flatten().reshape(-1, 1))
    projection_nn = mlp.predict(projection_scaled)
    projection_nn = projection_nn.reshape(projection.shape)
    ggems_primary_only_nn.append(projection_nn)

# scale the ggems neural network projections to match the fastcat projections
ggems_fastcat_nn = normalize_mean_and_std(
    np.array(ggems_primary_only_nn), np.array(ggems_primary_only))

# %%
perc_diff_primary = (np.array(ggems_primary_only) -
                     np.array(ggems_fastcat_nn[-1::-1]))/np.max(ggems_primary_only)*100

# plt.figure()
# ctrl = pli.hyperslicer(np.array(perc_diff_primary), cmap='bwr',
#                        vmax=5, vmin=-5)

# %%
phantom_projections = ggems_fastcat_nn

# Downsize the perc_diff using the downsize_block function
perc_diff = (np.array(ggems_scatter_denoised) -
             np.array(ggems_scatter_projections))/np.max(ggems_scatter_projections)*100
perc_diff_small = []
for i in range(len(perc_diff)):
    perc_diff_small.append(downsize_block(perc_diff[i], 16))

# Check pep8 again and again
# Plot the ggems projections
fig, (axes) = plt.subplots(ncols=2, nrows=3, figsize=(5.8, 10))

# Plot the denoised ggems projections
controls = pli.hyperslicer(np.array(ggems_scatter_denoised),
                           ax=axes[1][0], cmap='jet', vmax=np.percentile(np.array(ggems_scatter_denoised), 99),
                           vmin=np.percentile(np.array(ggems_scatter_denoised), 1), play_buttons=True)
axes[1][0].set_title('Denoised GGEMS scatter')

ggems_primary_only = np.array(
    ggems_primary_projections) - np.array(ggems_scatter_projections)
# Plot the ggems projections
c2 = pli.hyperslicer(np.array(ggems_primary_only), ax=axes[0][1], cmap='gray', controls=controls,
                     vmax=np.percentile(np.array(ggems_primary_only), 99),
                     vmin=np.percentile(np.array(ggems_primary_only), 1))
axes[0][1].set_title('GGEMS Primary')

# Plot the phantom phantom_projections
c1 = pli.hyperslicer(np.array(phantom_projections)[-1::-1], ax=axes[1][1], cmap='gray', controls=controls,
                     vmax=np.percentile(np.array(phantom_projections), 99),
                     vmin=np.percentile(np.array(phantom_projections), 1))
axes[1][1].set_title('Analytical Primary')

# Plot the difference between the ggems and phantom projections
perc_diff_primary = (np.array(ggems_primary_only) -
                     np.array(phantom_projections[-1::-1]))/np.max(phantom_projections)*100

c4 = pli.hyperslicer(np.array(perc_diff_primary), ax=axes[2][1], cmap='bwr', controls=controls,
                     vmax=5, vmin=-5)
axes[2][1].set_title('Perc. Diff. [%]')
# Add a colorbar
plt.colorbar(ax=axes[2][1])

# Plot the ggems projections
c2 = pli.hyperslicer(np.array(ggems_scatter_projections), ax=axes[0][0], cmap='jet', controls=controls,
                     vmax=np.percentile(
                         np.array(ggems_scatter_projections), 99),
                     vmin=np.percentile(np.array(ggems_scatter_projections), 1))

axes[0][0].set_title('GGEMS Scatter')

# Plot the ggems primary projections
c3 = pli.hyperslicer(np.array(perc_diff_small),
                     ax=axes[2][0], cmap='bwr', vmax=5, vmin=-5, controls=controls)
plt.colorbar(ax=axes[2][0])
axes[2][0].set_title('Perc. Diff. [%]')
plt.tight_layout()
# Turn off the axes
for ax in axes.flatten():
    ax.axis('off')

plt.show(block=True)
# Define a function that given an angle and radius returns x and y coordinates
# def f(axis0,radius=220,offset=0,x0=256,y0=256,na=90):
#     angle = np.deg2rad(axis0*360/na)
#     x = radius * np.cos(angle+offset) + x0
#     y = radius * np.sin(angle+offset) + y0
#     return np.array([[x,y],[x,y],[x,y]])

# iplt.plot(f, ax=axes[4], a=(0.1,10), b=(0.1,10), parametric=True,ylim=[0,1],xlim=[1,na],play_buttons=True)
# plt.imshow(phantom.phantom[50, :, :], cmap='gray')
# iplt.scatter(f, ax=axes[3][0], controls=controls,play_buttons=True,c='r',marker='>',parametric=True,)

# Add a label in the image saying source position
# axes[3].text(50, 50, 'Source Position', color='r', fontsize=12)


# %%
# Save the figure as a gif using mpl_interactions
# save as a gif
# anim = controls.save_animation("phantoms_ggems_analytical+denoised.gif", fig, "axis0", interval=120)
