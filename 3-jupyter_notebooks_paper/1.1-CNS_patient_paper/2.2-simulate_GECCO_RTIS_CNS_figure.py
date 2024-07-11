#!/usr/bin/env python
# coding: utf-8

# In[2]:


# get_ipython().run_line_magic('pylab', 'widget')
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')
# %load_ext memory_profiler


# ## GECCO CNS Patient

# In[3]:


# Read the mhd file from data
from gecco import patient_data
import gecco as fc
import numpy as np
from gecco.utils import nrrd_to_mhd
import mpl_interactions as pli

import matplotlib.pyplot as plt
from scipy.ndimage import zoom, gaussian_filter
import SimpleITK as sitk


# In[4]


nrrd_file = '/media/jericho/T7/dfci_laptop_backup/Documents/christian_patient_data/BRAIN/2_Stereo_CNS_Scan.nrrd'
phantom_rtis = patient_data.patient_phantom(nrrd_file, 1e7)


# In[282]:


spectrum = fc.calculate_spectrum_sp(100,12)

# Beam filters
spectrum.filter('Be', 1.5)
spectrum.filter('Al', 2.75)
spectrum.filter('Ti', 0.89)

# Detector filters
spectrum.filter('Al', 3.7)
spectrum.filter('C', 3.8*(2/1.7)) # Difference in density
phantom_rtis.initialize_fastmc(1, spectrum)


# In[283]:


phantom_rtis.phantom = phantom_rtis.phantom[:,60:,:]
phantom_rtis.density = phantom_rtis.density[:,60:,:]


# In[284]:


import numpy as np

phantom_rtis.phantom = phantom_rtis.phantom[139]
phantom_rtis.density = phantom_rtis.density[139]

# insert a new axis to the phantom
phantom_rtis.phantom = phantom_rtis.phantom[np.newaxis, ...]
phantom_rtis.density = phantom_rtis.density[np.newaxis, ...]

phantom_rtis.geomet.nVoxel = np.array([1,452, 512])
phantom_rtis.geomet.dVoxel = np.array([0.8, 0.8, 0.8])
phantom_rtis.geomet.sVoxel = phantom_rtis.geomet.dVoxel * phantom_rtis.geomet.nVoxel

phantom_rtis.geomet.nDetector = np.array([1, 512]) 
phantom_rtis.geomet.dDetector = np.array([phantom_rtis.geomet.dVoxel[0], 0.8])
phantom_rtis.geomet.sDetector = phantom_rtis.geomet.dDetector * phantom_rtis.geomet.nDetector

phantom_rtis.geomet.mode = "parallel"


# In[285]:


# %%timeit
# phantom_rtis.bowtie_file = '/home/jericho/Software/gecco/gecco/data/bowties/no_bowtie.dat'
phantom_rtis.retain_partial_calcs = True
phantom_rtis.run_gecco(1e10,815,conv_on=False,filter_on=False)


phantom_rtis.reweight(100,scat=0.05,mAs=400)


# In[321]:


img = phantom_rtis.img.squeeze()
water = np.mean(img[236:250,285:300])
air = np.mean(img[120:180,60:140])
# convert to HU using the water calibration
img = (img - water)/(water - air) * 1000
# img = gaussian_filter(img,1)


img_noise = img #np.load('815_proj_HU_noise.npy')
# img = img #np.load('815_proj_HU_no_noise.npy')
img = gaussian_filter(img,1)
img2 = gaussian_filter(img,2)
img_noise = gaussian_filter(img_noise,.5)

plt.figure(figsize=(8,8))

cbct_hu_clean = zoom(cbct_hu[79:81].mean(axis=0),0.511/0.761)
cbct_hu2 = gaussian_filter(cbct_hu_clean,2)
index = 115
index2 = 124
crop = [60,80,88,90]

plt.subplot(2,2,1)
plt.imshow(img_noise[crop[0]:-crop[1],crop[2]:-crop[3]], cmap='gray', vmin=-200, vmax=200)
# indicate the profile with a red dotted axis horizontal line
plt.axhline(135, color='darkorange', linestyle=':')
plt.axvline(index2, color='indianred', linestyle=':')
plt.xlabel('Pixels')
plt.ylabel('Pixels')
plt.title('a) RTIS')
ax = plt.gca()
ax_inset = zoomed_inset_axes(ax, 2, loc='lower right')
ax_inset.imshow(img_noise[crop[0]:-crop[1],crop[2]:-crop[3]], cmap='gray', vmin=-200, vmax=200)
ax_inset.set_ylim(70,30)
ax_inset.set_xlim(150,190)
ax_inset.axis('off')
# plt.axis('off')
mark_inset(ax, ax_inset, loc1=1, loc2=3, fc="none", ec="0.5")
plt.subplot(2,2,3)
plt.imshow(cbct_hu_clean[15:-20,10:-30], cmap='gray', vmin=-200, vmax=200)
plt.axhline(135, color='forestgreen', linestyle=':')
plt.axvline(index, color='cornflowerblue', linestyle=':')
plt.xlabel('Pixels')
plt.ylabel('Pixels')
plt.title('c) OBI')

ax = plt.gca()
ax_inset = zoomed_inset_axes(ax, 2, loc='lower right')
ax_inset.imshow(cbct_hu_clean[15:-20,10:-30], cmap='gray', vmin=-200, vmax=200)
ax_inset.set_ylim(70,30)
ax_inset.set_xlim(140,180)
ax_inset.axis('off')
# plt.axis('off')
mark_inset(ax, ax_inset, loc1=1, loc2=3, fc="none", ec="0.5")

plt.subplot(2,2,2)
profile = img[300,:]

# x1 = np.arange(crop[2], img.shape[1]-crop[3])
# x2 = np.linspace(0, 512,cbct_hu2.shape[1])
plt.plot(img[135+crop[0],crop[2]:-crop[3]], label='RTIS', c='darkorange')
plt.plot(cbct_hu2[135 + 15], label='OBI', c = 'forestgreen', linestyle='--')
plt.xlim(30,300)
# plt.xlim(100,410)
plt.legend()
plt.title('b) Horizontal profile')
plt.xlabel('Pixels')
plt.ylabel('HU')
plt.grid('on')
plt.tight_layout()

plt.subplot(2,2,4)
plt.plot(img2[crop[0]:-crop[1],index2+crop[2]], label='RTIS', c='indianred')
plt.plot(cbct_hu2[15:-20,index+12], label='OBI', c = 'cornflowerblue', linestyle='--')

# plt.xlim(100,410)
plt.legend()
plt.title('d) Vertical profile')
plt.xlabel('Pixels')
plt.ylabel('HU')
plt.grid('on')
plt.tight_layout()
# Interpolate the profile to the same length
from scipy.interpolate import interp1d

# f1 = interp1d(x1, img[199,crop[2]:-crop[3]])
# f2 = interp1d(x2, cbct_hu2[127,10:-20])

# x = np.linspace(100,410,512)
# plt.figure()
# plt.plot(x, f1(x), label='GECCO', c='darkorange')
# plt.plot(x, f2(x), label='CBCT', c = 'forestgreen', linestyle='--')
# plt.legend()
# plt.colorbar(label='HU')   
prof = np.abs(img[135+crop[0],crop[2]:-crop[3]] - cbct_hu2[135 + 15,:-10])
# Calculate the difference between the two profiles
mean_diff = np.mean(prof[img[135+crop[0],crop[2]:-crop[3]]>-250])
std_diff = np.std(np.abs(img[135+crop[0],crop[2]:-crop[3]] - cbct_hu2[135 + 15,:-10]))

# prof2 = np.abs(img2[crop[0]:-crop[1],index2+crop[2]] - cbct_hu2[15:-20,index+12])
# # Calculate the difference between the two profiles
# mean_diff2 = np.mean(prof2[img2[crop[0]:-crop[1],index2+crop[2]]>-250])
# std_diff2 = np.std(np.abs(img2[crop[0]:-crop[1],index2+crop[2]] - cbct_hu2[15:-20,index+12]))
                   
plt.savefig('figure_4_CNS_RTIS.png', dpi=300)
print(f'Mean difference: {mean_diff:.2f} HU')
print(f'Standard deviation: {std_diff:.2f} HU')
# print(f'Mean difference: {mean_diff2:.2f} HU')
# print(f'Standard deviation: {std_diff2:.2f} HU')


# ### For writing new spectra to the database

# In[245]:


# import os

# data_dir = '/home/jericho/Software/gecco/gecco/data/kV_spectra'

# for kV in range(60,141):

#     spec = fc.calculate_spectrum_sp(kV,14) # initialize the spectrum
#     spec.filter('Be', 1.5)
#     spec.filter('Al', 2.75)
#     spec.filter('Ti', 0.89)

#     # Detector filters
#     spec.filter('Al', 3.7)
#     spec.filter('C', 3.8*(2/1.7))

#     spec.write_dat_file(os.path.join(
#                 data_dir, f"{kV}.dat"),normalize=False)

