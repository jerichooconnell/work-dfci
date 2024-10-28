import matplotlib.pyplot as plt
import scipy.io
import numpy as np

# Creates a mask of misbehaving pixels and generate and applies gain maps/mask

# Load mask
base_path = "/home/jericho/1-Workspace/9-PCCT_Magdalena_results/"
filebasemask = base_path + "S1728_PeptoBismol_Mask_20_30_76_100_114_120/"
filebaseblank = base_path + "S1728_PeptoBismol_AirScan_20_30_76_100_114_120/"
filebaseStent = base_path + "S1728_PeptoBismol_BiAtt_20_30_76_100_114_120/"
# filebaseblank = "M:/DetCal/Calibrations080124/S1728_AirSweepA120kVp20_30_50_70_90_120/"
# filebaseStent = "M:/DetCal/Calibrations080124/S1728_MaskSweepCaCo_120kVp_20_30_50_70_90_120/"
# outfile = "./DSImgs/90kVpSweeps/"
file = "M62638-A0.mat"

# Load data
nMeas = 255 - 50 + 1
imageBin1 = scipy.io.loadmat(f"{filebasemask}Bin1.mat")['imageBin1']
imageBin2 = scipy.io.loadmat(f"{filebasemask}Bin2.mat")['imageBin2']
imageBin3 = scipy.io.loadmat(f"{filebasemask}Bin3.mat")['imageBin3']
imageBin4 = scipy.io.loadmat(f"{filebasemask}Bin4.mat")['imageBin4']
imageBin5 = scipy.io.loadmat(f"{filebasemask}Bin5.mat")['imageBin5']
imageBin6 = scipy.io.loadmat(f"{filebasemask}Bin6.mat")['imageBin6']
imageBinAll = scipy.io.loadmat(f"{filebasemask}BinAll.mat")['imageBinAll']

imageBin1blank = scipy.io.loadmat(f"{filebaseblank}Bin1.mat")['imageBin1']
imageBin2blank = scipy.io.loadmat(f"{filebaseblank}Bin2.mat")['imageBin2']
imageBin3blank = scipy.io.loadmat(f"{filebaseblank}Bin3.mat")['imageBin3']
imageBin4blank = scipy.io.loadmat(f"{filebaseblank}Bin4.mat")['imageBin4']
imageBin5blank = scipy.io.loadmat(f"{filebaseblank}Bin5.mat")['imageBin5']
imageBin6blank = scipy.io.loadmat(f"{filebaseblank}Bin6.mat")['imageBin6']
imageBinAllblank = scipy.io.loadmat(
    f"{filebaseblank}BinAll.mat")['imageBinAll']

imageBin1obj = scipy.io.loadmat(f"{filebaseStent}Bin1.mat")['imageBin1']
imageBin2obj = scipy.io.loadmat(f"{filebaseStent}Bin2.mat")['imageBin2']
imageBin3obj = scipy.io.loadmat(f"{filebaseStent}Bin3.mat")['imageBin3']
imageBin4obj = scipy.io.loadmat(f"{filebaseStent}Bin4.mat")['imageBin4']
imageBin5obj = scipy.io.loadmat(f"{filebaseStent}Bin5.mat")['imageBin5']
imageBin6obj = scipy.io.loadmat(f"{filebaseStent}Bin6.mat")['imageBin6']
imageBinAllobj = scipy.io.loadmat(f"{filebaseStent}BinAll.mat")['imageBinAll']

# Threshold for mask
thresh = 0.25

# Assuming mapMask is a function defined elsewhere


def mapMask(image_bin, threshold):
    # Calculate mean and standard deviation along the first axis
    image_bin1_mean = np.mean(image_bin, axis=0)
    image_bin1_std = np.std(image_bin, axis=0)

    # Compute percentage variation
    image_perc = (image_bin1_std / image_bin1_mean) * 100

    # Replace NaN and Inf values with 100
    image_perc = np.nan_to_num(image_perc, nan=100, posinf=100, neginf=100)

    # Calculate the threshold
    global_threshold = np.mean(image_perc) + np.std(image_perc) * threshold
    n_row, n_col = image_perc.shape
    mask_map = np.zeros((n_row, n_col))

    # Apply the threshold to create the mask
    for i in range(n_row):
        for j in range(n_col):
            if image_perc[i, j] > global_threshold:
                mask_map[i, j] = 1

    # Handle corners and edges separately
    for i in range(n_row):
        for j in range(n_col):
            if i <= 2 and j <= 2 or i <= 2 and j >= n_col-2 or i >= n_row-2 and j >= n_col-2 or i >= n_row-2 and j <= 2:
                local = image_perc[max(0, i-2):min(n_row, i+3),
                                   max(0, j-2):min(n_col, j+3)]
                local_threshold = np.mean(local) + np.std(local) * threshold
                if image_perc[i, j] > local_threshold:
                    mask_map[i, j] = 1
            elif i <= 2 or j <= 2 or i >= n_row-2 or j >= n_col-2:
                local = image_perc[max(0, i-2):min(n_row, i+3),
                                   max(0, j-2):min(n_col, j+3)]
                local_threshold = np.mean(local) + np.std(local) * threshold
                if image_perc[i, j] > local_threshold:
                    mask_map[i, j] = 1
            else:
                local = image_perc[i-2:i+3, j-2:j+3]
                local_threshold = np.mean(local) + np.std(local) * threshold
                if image_perc[i, j] > local_threshold:
                    mask_map[i, j] = 1

    return mask_map


maskmap1 = mapMask(imageBin1, thresh)
maskmap2 = mapMask(imageBin2, thresh)
maskmap3 = mapMask(imageBin3, thresh)
maskmap4 = mapMask(imageBin4, thresh)
maskmap5 = mapMask(imageBin5, thresh)
maskmap6 = mapMask(imageBin6, thresh)
maskmapall = mapMask(imageBinAll, thresh)

# check if the image is 3d
if len(imageBin1.squeeze().shape) > 2:
    # Calculate mean images
    print('shape is 3d')
    imageBin1mean = np.mean(imageBin1, axis=1)
    imageBin2mean = np.mean(imageBin2, axis=1)
    imageBin3mean = np.mean(imageBin3, axis=1)
    imageBin4mean = np.mean(imageBin4, axis=1)
    imageBin5mean = np.mean(imageBin5, axis=1)
    imageBin6mean = np.mean(imageBin6, axis=1)
    imageBinAllmean = np.mean(imageBinAll, axis=1)
else:
    print("image is 2d")
    imageBin1mean = imageBin1.squeeze()
    imageBin2mean = imageBin2.squeeze()
    imageBin3mean = imageBin3.squeeze()
    imageBin4mean = imageBin4.squeeze()
    imageBin5mean = imageBin5.squeeze()
    imageBin6mean = imageBin6.squeeze()
    imageBinAllmean = imageBinAll.squeeze()
# import numpy as np

# Initialize maskarray
maskarray = np.array([[3, 2, 1, 2, 3],
                      [3, 2, 1, 2, 3],
                      [3, 2, 1, 2, 3],
                      [3, 2, 1, 2, 3],
                      [3, 2, 1, 2, 3]], dtype=float)

# Update maskarray values
for i in range(5):
    for j in range(5):
        maskarray[i, j] = 1 / np.sqrt((i - 2)**2 + (j - 2)**2)
maskarray[2, 2] = 0

# Assuming putonmask is a defined function


def putonmask(image, map, mask):
    # Get dimensions of the image and mask
    nRow, nCol = image.shape
    nRowm, nColm = mask.shape

    for i in range(nRow):
        for j in range(nCol):
            if map[i, j] == 1:
                if (i <= 2 and j <= 2) or (i <= 2 and j >= nCol - 1) or (i >= nRow - 1 and j >= nCol - 1) or (i >= nRow - 1 and j <= 2):
                    if i <= 2 and j <= 2:
                        if i == 1 and j == 1:
                            local = np.abs(
                                map[i:i+3, j:j+3] - 1) * mask[2:5, 2:5]
                            val = np.sum(
                                (image[i:i+3, j:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 1 and j == 2:
                            local = np.abs(
                                map[i:i+3, j-1:j+3] - 1) * mask[2:5, 1:5]
                            val = np.sum(
                                (image[i:i+3, j-1:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 2 and j == 1:
                            local = np.abs(
                                map[i-1:i+3, j:j+3] - 1) * mask[1:5, 2:5]
                            val = np.sum(
                                (image[i-1:i+3, j:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 2 and j == 2:
                            local = np.abs(
                                map[i-1:i+3, j-1:j+3] - 1) * mask[1:5, 1:5]
                            val = np.sum(
                                (image[i-1:i+3, j-1:j+3] * local) / np.sum(local))
                            image[i, j] = val
                    if i <= 2 and j >= nCol - 1:
                        if i == 1 and j == nCol:
                            local = np.abs(map[i:i+3, -3:] - 1) * mask[2:5, :3]
                            val = np.sum(
                                (image[i:i+3, -3:] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 1 and j == nCol - 1:
                            local = np.abs(map[i:i+3, -4:] - 1) * mask[2:5, :4]
                            val = np.sum(
                                (image[i:i+3, -4:] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 2 and j == nCol:
                            local = np.abs(
                                map[i-1:i+3, -3:] - 1) * mask[1:5, :3]
                            val = np.sum(
                                (image[i-1:i+3, -3:] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 2 and j == nCol - 1:
                            local = np.abs(
                                map[i-1:i+3, -4:] - 1) * mask[1:5, :4]
                            val = np.sum(
                                (image[i-1:i+3, -4:] * local) / np.sum(local))
                            image[i, j] = val
                    if i >= nRow - 1 and j >= nCol - 1:
                        if i == nRow and j == nCol:
                            local = np.abs(map[-3:, -3:] - 1) * mask[:3, :3]
                            val = np.sum(
                                (image[-3:, -3:] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow and j == nCol - 1:
                            local = np.abs(map[-3:, -4:] - 1) * mask[:3, :4]
                            val = np.sum(
                                (image[-3:, -4:] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow - 1 and j == nCol:
                            local = np.abs(map[-4:, -3:] - 1) * mask[:4, :3]
                            val = np.sum(
                                (image[-4:, -3:] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow - 1 and j == nCol - 1:
                            local = np.abs(map[-4:, -4:] - 1) * mask[:4, :4]
                            val = np.sum(
                                (image[-4:, -4:] * local) / np.sum(local))
                            image[i, j] = val
                    if i >= nRow - 1 and j <= 2:
                        if i == nRow and j == 1:
                            local = np.abs(map[-3:, j:j+3] - 1) * mask[:3, 2:5]
                            val = np.sum(
                                (image[-3:, j:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow and j == 2:
                            local = np.abs(
                                map[-3:, j-1:j+3] - 1) * mask[:3, 1:5]
                            val = np.sum(
                                (image[-3:, j-1:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow - 1 and j == 1:
                            local = np.abs(map[-4:, j:j+3] - 1) * mask[:4, 2:5]
                            val = np.sum(
                                (image[-4:, j:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow - 1 and j == 2:
                            local = np.abs(
                                map[-4:, j-1:j+3] - 1) * mask[:4, 1:5]
                            val = np.sum(
                                (image[-4:, j-1:j+3] * local) / np.sum(local))
                            image[i, j] = val
                elif i <= 2 or j <= 2 or i >= nRow - 1 or j >= nCol - 1:
                    if i <= 2:
                        if i == 1:
                            local = np.abs(
                                map[i:i+3, j-2:j+3] - 1) * mask[2:5, :5]
                            val = np.sum(
                                (image[i:i+3, j-2:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == 2:
                            local = np.abs(
                                map[i-1:i+3, j-2:j+3] - 1) * mask[1:5, :5]
                            val = np.sum(
                                (image[i-1:i+3, j-2:j+3] * local) / np.sum(local))
                            image[i, j] = val
                    if j <= 2:
                        if j == 1:
                            local = np.abs(
                                map[i-2:i+3, j:j+3] - 1) * mask[:5, 2:5]
                            val = np.sum(
                                (image[i-2:i+3, j:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if j == 2:
                            local = np.abs(
                                map[i-2:i+3, j-1:j+3] - 1) * mask[:5, 1:5]
                            val = np.sum(
                                (image[i-2:i+3, j-1:j+3] * local) / np.sum(local))
                            image[i, j] = val
                    if i >= nRow - 1:
                        if i == nRow:
                            local = np.abs(
                                map[-3:, j-2:j+3] - 1) * mask[:3, :5]
                            val = np.sum(
                                (image[-3:, j-2:j+3] * local) / np.sum(local))
                            image[i, j] = val
                        if i == nRow - 1:
                            local = np.abs(
                                map[-4:, j-2:j+3] - 1) * mask[:4, :5]
                            val = np.sum(
                                (image[-4:, j-2:j+3] * local) / np.sum(local))
                            image[i, j] = val
                    if j >= nCol - 1:
                        if j == nCol:
                            local = np.abs(
                                map[i-2:i+3, -3:] - 1) * mask[:5, :3]
                            val = np.sum(
                                (image[i-2:i+3, -3:] * local) / np.sum(local))
                            image[i, j] = val
                        if j == nCol - 1:
                            local = np.abs(map[i-2:i+3, -4:]
                                           - 1) * mask[:5, :4]
                            val = np.sum(
                                (image[i-2:i+3, -4:] * local) / np.sum(local))
                            image[i, j] = val
                else:
                    local = np.abs(map[i-2:i+3, j-2:j+3] - 1) * mask[:5, :5]
                    val = np.sum(
                        (image[i-2:i+3, j-2:j+3] * local) / np.sum(local))
                    image[i, j] = val

    return image


# Calculate corrected masks
correctedmask1 = putonmask(imageBin1mean, maskmap1, maskarray)
correctedmask2 = putonmask(imageBin2mean, maskmap2, maskarray)
correctedmask3 = putonmask(imageBin3mean, maskmap3, maskarray)
correctedmask4 = putonmask(imageBin4mean, maskmap4, maskarray)
correctedmask5 = putonmask(imageBin5mean, maskmap5, maskarray)
correctedmask6 = putonmask(imageBin6mean, maskmap6, maskarray)
correctedmaskall = putonmask(imageBinAllmean, maskmapall, maskarray)

# Calculate gain maps
gainmap1 = correctedmask1 / np.mean(correctedmask1)
gainmap2 = correctedmask2 / np.mean(correctedmask2)
gainmap3 = correctedmask3 / np.mean(correctedmask3)
gainmap4 = correctedmask4 / np.mean(correctedmask4)
gainmap5 = correctedmask5 / np.mean(correctedmask5)
gainmap6 = correctedmask6 / np.mean(correctedmask6)
gainmapall = correctedmaskall / np.mean(correctedmaskall)

# Get dimensions
nangle = imageBin1obj.shape[0]
nrow = imageBin1blank.shape[1]
ncol = imageBin1blank.shape[2]

# Initialize output arrays
imageout = np.zeros((nangle, nrow, ncol))
imageoutblank = np.zeros((nangle, nrow, ncol))


# Process each bin
for bb in range(1, 8):
    iii = 0
    if bb == 1:
        for ii in range(nangle):
            if iii == imageBin1blank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBin1blank[iii, :, :], maskmap1, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBin1obj[ii, :, :], maskmap1, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmap1[jj, kk]
                    imageout[ii, jj, kk] /= gainmap1[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlank1.npy", imageoutblank)
        np.save(filebaseStent + "Projection1.npy", imageout)
        plt.figure(1)
        plt.imshow(imageout[0, :, :])
        plt.show()
    elif bb == 2:
        for ii in range(nangle):
            if iii == imageBin2blank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBin2blank[iii, :, :], maskmap2, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBin2obj[ii, :, :], maskmap2, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmap2[jj, kk]
                    imageout[ii, jj, kk] /= gainmap2[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlank2.npy", imageoutblank)
        np.save(filebaseStent + "Projection2.npy", imageout)
        plt.figure(2)
        plt.imshow(imageout[0, :, :])
        plt.show()
    elif bb == 3:
        for ii in range(nangle):
            if iii == imageBin3blank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBin3blank[iii, :, :], maskmap3, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBin3obj[ii, :, :], maskmap3, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmap3[jj, kk]
                    imageout[ii, jj, kk] /= gainmap3[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlank3.npy", imageoutblank)
        np.save(filebaseStent + "Projection3.npy", imageout)
        plt.figure(3)
        plt.imshow(imageout[0, :, :])
        plt.show()
    elif bb == 4:
        for ii in range(nangle):
            if iii == imageBin4blank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBin4blank[iii, :, :], maskmap4, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBin4obj[ii, :, :], maskmap4, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmap4[jj, kk]
                    imageout[ii, jj, kk] /= gainmap4[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlank4.npy", imageoutblank)
        np.save(filebaseStent + "Projection4.npy", imageout)
        plt.figure(4)
        plt.imshow(imageout[0, :, :])
        plt.show()
    elif bb == 5:
        for ii in range(nangle):
            if iii == imageBin5blank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBin5blank[iii, :, :], maskmap5, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBin5obj[ii, :, :], maskmap5, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmap5[jj, kk]
                    imageout[ii, jj, kk] /= gainmap5[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlank5.npy", imageoutblank)
        np.save(filebaseStent + "Projection5.npy", imageout)
        plt.figure(5)
        plt.imshow(imageout[0, :, :])
        plt.show()
    elif bb == 6:
        for ii in range(nangle):
            if iii == imageBin6blank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBin6blank[iii, :, :], maskmap6, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBin6obj[ii, :, :], maskmap6, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmap6[jj, kk]
                    imageout[ii, jj, kk] /= gainmap6[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlank6.npy", imageoutblank)
        np.save(filebaseStent + "Projection6.npy", imageout)
        plt.figure(6)
        plt.imshow(imageout[0, :, :])
        plt.show()
    elif bb == 7:
        for ii in range(nangle):
            if iii == imageBinAllblank.shape[0]:
                iii = 0
            imageoutblank[ii, :, :] = putonmask(
                imageBinAllblank[iii, :, :], maskmapall, maskarray)
            imageout[ii, :, :] = putonmask(
                imageBinAllobj[ii, :, :], maskmapall, maskarray)
            for jj in range(nrow):
                for kk in range(ncol):
                    imageoutblank[ii, jj, kk] /= gainmapall[jj, kk]
                    imageout[ii, jj, kk] /= gainmapall[jj, kk]
            iii += 1
        np.save(filebaseStent + "ProjectionBlankall.npy", imageoutblank)
        np.save(filebaseStent + "Projectionall.npy", imageout)
        plt.figure(7)
        plt.imshow(imageout[0, :, :])
        plt.show()
