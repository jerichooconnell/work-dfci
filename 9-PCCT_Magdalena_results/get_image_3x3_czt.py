import matplotlib.cm as cm
import matplotlib.pyplot as plt
import argparse
import numpy as np
import scipy.io


def get_image_3x3_czt(filenamebase, bin):
    filearray = [
        ["M62638-A0.mat", "M62638-A1.mat"],
        ["M62639-A0.mat", "M62639-A1.mat"],
        ["M62641-A0.mat", "M62641-A1.mat"],
        ["M62646-A0.mat", "M62646-A1.mat"],
        ["M62651-A0.mat", "M62651-A1.mat"],
        ["M62652-A0.mat", "M62652-A1.mat"],
        ["M62653-A0.mat", "M62653-A1.mat"],
        ["M62654-A0.mat", "M62654-A1.mat"]
    ]

    datain = scipy.io.loadmat(f"{filenamebase}{filearray[0][0]}")
    cc_data = datain['cc_struct']['data'][0][0]['cc_data'][0][0]

    nframes = cc_data.shape[0]
    rows = cc_data.shape[3]
    cols = cc_data.shape[4]

    output = np.zeros((nframes, 192, 72))

    for j in range(len(filearray)):
        for i in range(len(filearray[j])):
            datain = scipy.io.loadmat(f"{filenamebase}{filearray[j][i]}")
            cc_data = datain['cc_struct']['data'][0][0]['cc_data'][0][0]
            for k in range(nframes):
                if i == 0:
                    output[k, 24*(j):24+24*(j), 36*(i):36+36*(i)
                           ] = np.flipud(np.fliplr(cc_data[k, bin, 0, :, :]))
                else:
                    output[k, 24*(j):24+24*(j), 36*(i):36 +
                           36*(i)] = cc_data[k, bin, 0, :, :]

    return output


# Meant for preloading images for fast post processing
parser = argparse.ArgumentParser(
    description='Preload images for post processing')
parser.add_argument('filebaselow', type=str, help='File base low')
args = parser.parse_args()

filebaselow = args.filebaselow

# Stitches together the asics
imageBin1 = get_image_3x3_czt(filebaselow, 0)
imageBin2 = get_image_3x3_czt(filebaselow, 1)
imageBin3 = get_image_3x3_czt(filebaselow, 2)
imageBin4 = get_image_3x3_czt(filebaselow, 3)
imageBin5 = get_image_3x3_czt(filebaselow, 4)
imageBin6 = get_image_3x3_czt(filebaselow, 5)
imageBinAll = get_image_3x3_czt(filebaselow, 6)

# Save the images
scipy.io.savemat(f"{filebaselow}Bin1.mat", {"imageBin1": imageBin1})
scipy.io.savemat(f"{filebaselow}Bin2.mat", {"imageBin2": imageBin2})
scipy.io.savemat(f"{filebaselow}Bin3.mat", {"imageBin3": imageBin3})
scipy.io.savemat(f"{filebaselow}Bin4.mat", {"imageBin4": imageBin4})
scipy.io.savemat(f"{filebaselow}Bin5.mat", {"imageBin5": imageBin5})
scipy.io.savemat(f"{filebaselow}Bin6.mat", {"imageBin6": imageBin6})
scipy.io.savemat(f"{filebaselow}BinAll.mat", {"imageBinAll": imageBinAll})

# Save to npy
np.save(f"{filebaselow}Bin1.npy", imageBin1)
np.save(f"{filebaselow}Bin2.npy", imageBin2)
np.save(f"{filebaselow}Bin3.npy", imageBin3)
np.save(f"{filebaselow}Bin4.npy", imageBin4)
np.save(f"{filebaselow}Bin5.npy", imageBin5)
np.save(f"{filebaselow}Bin6.npy", imageBin6)
np.save(f"{filebaselow}BinAll.npy", imageBinAll)


# Save them as pngs

for i in range(imageBin1.shape[0]):
    plt.imshow(imageBin1[i, :, :], cmap=cm.gray)
    plt.savefig(f"{filebaselow}Bin1_{i}.png")
