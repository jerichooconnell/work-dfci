
import numpy as np
import struct

import glob


def main():
    # sample_file = '/home/jericho/SA_10_52/Temp/reformatted/2024-01-20_16h-55m-58s_080kVp_30mAs_0915_images_Bin2x8LowGain/2nd_Layer/2024-01-20_16h-55m-58s_2nd_Layer_0000.xim'
    # sample_file_base = '/home/jericho/SA_10_52/Temp/reformatted/2024-01-20_16h-55m-58s_080kVp_30mAs_0915_images_Bin2x8LowGain'
    # look at 2024-01-20_16h-42m-25s_080kVp_30mAs_0915_images_Bin2x8LowGain
    # sample_file_base = '/home/jericho/SA_10_52/Temp/reformatted/2024-01-20_16h-42m-25s_080kVp_30mAs_0915_images_Bin2x8LowGain'
    # look at 2024-01-20_16h-37m-15s_080kVp_10mAs_0915_images_Bin2x8LowGain
    sample_file_base = '/home/jericho/SA_10_52/Temp/reformatted/2024-01-20_16h-37m-15s_080kVp_10mAs_0915_images_Bin2x8LowGain'
    # test_xim = XIMFile(sample_file)

    # for k, v in test_xim.header.items():

    #     print(k, v)
    print('Loading first layer')
    sample_file_fl = sample_file_base + '/1st_Layer/*.xim'
    sample_file_sl = sample_file_base + '/2nd_Layer/*.xim'

    xmf_list = [XIMFile(s) for s in sorted(glob.glob(sample_file_fl))]

    imgs = [s.pixel_data for s in xmf_list]
    headers = [s.header for s in xmf_list]

    np.save(f'projections/{sample_file_base.split(r"/")[-1]}_1st_Layer', imgs)
    np.save(
        f'projections/{sample_file_base.split(r"/")[-1]}_1st_Layer_headers', headers)

    print('Loading second layer')
    xmf_list = [XIMFile(s) for s in sorted(glob.glob(sample_file_sl))]
    imgs = [s.pixel_data for s in xmf_list]
    headers = [s.header for s in xmf_list]

    np.save(f'projections/{sample_file_base.split(r"/")[-1]}_2nd_Layer', imgs)
    np.save(
        f'projections/{sample_file_base.split(r"/")[-1]}_2nd_Layer_headers', headers)


class XIMFile(object):

    def __init__(self, file_name, load_pixel_data=True):
        self.file_name = file_name

        with open(self.file_name, 'rb') as fid:

            short_header = self.read_short_header(fid)

            self.nx = short_header['nx']
            self.ny = short_header['ny']
            self.is_compressed = short_header['compressed']
            self.bytes_per_pix = short_header['bytes_per_pix']

            self.pixel_data = self.load_pixel_data(
                fid, self.nx, self.ny, self.bytes_per_pix, self.is_compressed, read_pixels=load_pixel_data)

            if self.pixel_data is not None:
                self.pixel_data = np.flipud(self.pixel_data).astype(np.float32)
            hist = self.read_histogram(fid)

            long_head = self.test_get_long_header(fid)

        self.header = {}
        self.header.update(short_header)
        self.header.update(hist)
        self.header.update(long_head)
        self.property_keys = list(long_head.keys())

        self.total_dose = self.get_total_dose()

    def get_total_dose(self):
        return None

    def __getitem__(self, item):
        try:
            return self.header[item][2]
        except TypeError:
            return self.header[item]

    def __setitem__(self, key, value):
        item = list(self.header[key])
        item[2] = value
        self.header[key] = tuple(item)

    def set_pixel_data(self, pix_array):

        self.pixel_data = pix_array

        ny, nx = np.shape(pix_array)
        self.header['nx'] = nx
        self.header['ny'] = ny

        self.nx = nx
        self.ny = ny

    def set_header_val(self, tag, value):

        old_head = list(self.header[tag])
        old_head[2] = value
        self.header[tag] = old_head

    @classmethod
    def from_list(cls, file_list, load_pixel_data=True, threads=None):
        """

        :rtype: list of XIMFile
        """

        if threads is None:
            import multiprocessing as mp
            threads = mp.cpu_count() - 1

        import pathos.multiprocessing as mp
        pool = mp.Pool(threads)  # Create a multiprocessing Pool

        params = [(f, load_pixel_data) for f in file_list]

        res = []
        for p in params:
            # proces data_inputs iterable with pool)
            res.append(pool.apply_async(cls, args=p))

        pool.close()
        pool.join()

        return [s.get() for s in res]

        # return pool.map(SingleRunner(cls, load_pixel_data), file_list)

    @classmethod
    def from_directory(cls, xim_directory, load_pixel_data=True, threads=None):
        import pathos.multiprocessing as mp
        import os
        if threads is None:
            threads = mp.cpu_count() - 1

        # JO vhanged list_files_by_wildcard to glob
        xim_files = sorted(glob.glob(os.path.join(xim_directory, '*.xim')))

        return cls.from_list(xim_files, load_pixel_data=load_pixel_data, threads=threads)

    @staticmethod
    def read_short_header(fid):

        short_header = {}

        # unsure of purpose
        import struct
        short_header['sh1'] = struct.unpack('<8B', fid.read(8))
        short_header['sh2'] = struct.unpack('<i', fid.read(4))[0]

        # pixel array dimensions
        short_header['nx'] = struct.unpack('<i', fid.read(4))[0]
        short_header['ny'] = struct.unpack('<i', fid.read(4))[0]

        # pixel bits/bytes , why both?
        short_header['bits_per_pix'] = struct.unpack('<i', fid.read(4))[0]
        short_header['bytes_per_pix'] = struct.unpack('<i', fid.read(4))[0]

        # compression
        short_header['compressed'] = struct.unpack('<i', fid.read(4))[0]

        return short_header

    def write(self, file_name):

        with open(file_name, 'wb') as fid:
            self.write_short_header(fid)
            self.write_pixel_data(fid)
            self.write_hist(fid)

            # prop_keys =tag_names = fieldnames(self.header);

            import struct
            fid.write(struct.pack('<i', len(self.property_keys)))

            for key in self.property_keys:

                nl, type, value = self.header[key]

                self.write_meta_data(fid, key, value, nl, type)

                # tag = tag_names
                # {i};
                # val = self.header.(tag);
                # tagdat = self.tag_data.(tag);
                # taglen = tagdat(1);
                # tagtype = tagdat(2);

    def write_short_header(self, fid):

        self.header['sh2'] = 1

        import struct
        fid.write(struct.pack('<8B', *self.header['sh1']))
        fid.write(struct.pack('<i', self.header['sh2']))
        fid.write(struct.pack('<i', self.header['nx']))
        fid.write(struct.pack('<i', self.header['ny']))
        fid.write(struct.pack('<i', 32))
        # fid.write(struct.pack('<i', 20))
        fid.write(struct.pack('<i', 4))
        fid.write(struct.pack('<i', 0))

    @classmethod
    def load_pixel_data(cls, fid, width, height, bytes_per_pixel, is_compressed, read_pixels=True):
        '''
        Pixel values in an HND image is stored in pixelData field. Pixel data are either
        compressed or uncompressed which can be determined by the "Compression indicator"
        field in the header data.
        '''

        # Image pixels are stored uncompressed in the xim image file.
        # pprint(self.ximHeader)
        if not is_compressed:
            # Read in int4 (32 bit) image pixe values
            import struct
            uncompressedPixelBufferSize = struct.unpack('<i', fid.read(4))[0]

            if read_pixels:
                # Read in pixel values in 1D array
                uncompressedPixelBuffer = np.asarray(struct.unpack('<%ii' % (uncompressedPixelBufferSize / 4),
                                                                   fid.read(uncompressedPixelBufferSize)))
                uncompressedPixelBuffer = np.reshape(
                    uncompressedPixelBuffer, (height, width))
                return uncompressedPixelBuffer
            else:
                fid.seek(uncompressedPixelBufferSize, 1)
                return None

        # Decompress the pixelData using HND decompression algorithm.
        else:
            import struct
            LUTSize = struct.unpack('<i', fid.read(4))[0]  # Lookup table size
            LUT = np.asarray(struct.unpack('<%iB' %
                             LUTSize, fid.read(LUTSize)))  # Lookup table
            # Compressed pixel buffer size
            nComp = struct.unpack('<i', fid.read(4))[0]

            if read_pixels:
                compressedImage = np.asarray(struct.unpack(
                    '<%ib' % nComp, fid.read(nComp)), dtype=np.int8)
                uncompressedPixelBuffer, diff = cls.test_uncompress(
                    compressedImage, width, height, bytes_per_pixel, LUT)  # Uncompress the pixel data

                uncompressedBufferSize = struct.unpack('<i', fid.read(4))[
                    0]  # Uncompressed pixel image size

                del compressedImage, diff, LUT

                return uncompressedPixelBuffer
            else:
                fid.seek(nComp, 1)
                fid.seek(4, 1)
                return None

        # Reshape uncompressed image into 2D array

    def write_pixel_data(self, fid):
        nData = self.nx*self.ny*4
        import struct
        fid.write(struct.pack('<i', nData))
        data = np.flipud(self.pixel_data.astype(np.int32)).flatten()
        fid.write(struct.pack('<'+repr(self.nx*self.ny)+'i', *data))

    def write_hist(self, fid):
        import struct
        fid.write(struct.pack('<i', self.header['hist_NumberOfBins']))
        fid.write(struct.pack('<%si' % self.header['hist_NumberOfBins'],
                              *self.header['hist_Value']))

    @classmethod
    def test_uncompress(self, compressed_image, nx, ny, bytes_per_pix, LUT, read_floats=False):

        mask = np.zeros((4, len(LUT)))

        for i in range(0, 4):

            mask[i, :] = np.bitwise_and(np.right_shift(LUT, 2 * (i)), 3)

        mask = mask.flatten(order='F')[0:nx * ny - nx - 1]

        ccomp = compressed_image[(nx + 1) * 4:]

        cmask = np.zeros((4, np.prod(np.shape(mask))), dtype=np.int8)
        cmask[0, :] = 1
        cmask[1, np.where(mask == 1)] = 1
        cmask[1:4, np.where(mask == 2)] = 1

        cdata = np.zeros(np.prod(np.shape(cmask)), dtype=np.int8)

        cdata[np.where(cmask.flatten(order='F') == 1)] = ccomp

        diff = cdata.view(np.uint32)

        indx = np.where(mask == 0)
        temp = diff[indx]
        temp[np.where(temp >= 128)] = temp[np.where(temp >= 128)
                                           ] + np.left_shift((np.power(2, 24) - 1), 8)
        diff[indx] = temp

        indx = np.where(mask == 1)
        temp = diff[indx]
        temp[np.where(temp >= np.power(2, 15))] = temp[np.where(
            temp >= np.power(2, 15))] + np.left_shift((np.power(2, 16) - 1), 16)
        diff[indx] = temp

        diff = diff.view(np.int32)

        data = np.zeros(nx * ny, dtype=np.int32)

        if read_floats:
            data[0:nx + 1] = compressed_image[0:(nx + 1) * 4].view(np.float32)
        else:
            data[0:nx + 1] = compressed_image[0:(nx + 1) * 4].view(np.int32)

        for i in range(nx+1, nx*ny):
            data[i] = data[i - nx] + data[i - 1] - \
                data[i - nx - 1] + diff[i - nx - 1]

        return np.reshape(data, (ny, nx)), LUT

    def test_compress(data):

        ny, nx = np.shape(data)
        data = data.flatten()

        diff = np.zeros(nx * ny - (nx + 1), dtype=np.int32)

        for i in range(nx + 1, nx * ny):
            diff[i - nx - 1] = data[i] + \
                data[i - nx - 1] - data[i - nx] - data[i - 1]

        first_row = data[0:nx + 1].view(np.int8)

        n_LUT = int(np.ceil(len(diff) / 4.0))

        lut_vals = np.zeros(n_LUT * 4, dtype=np.uint8)

        n1 = np.where((diff >= -128) & (diff <= 127))
        n2 = np.where(((diff > 127) & (diff < np.power(2, 15))) |
                      (diff < -128) & (diff >= -1 * np.power(2, 15)))
        n4 = np.where((diff > np.power(2, 15) - 1) |
                      (diff < -1 * np.power(2, 15)))

        lut_vals[n2] = 1
        lut_vals[n4] = 2

        # one_byte_arr = np.

        # n1 = np.where(lut_vals == 0)
        # n2 = np.where(lut_vals == 1)
        # n4 = np.where(lut_vals == 2)

        address = np.cumsum(np.power(2, lut_vals))

        comp_data = np.empty(
            (nx + 1) * 4 + (address[-1] - address[0]), dtype=np.int8)

        print(diff[n1])
        print(diff[n1].astype(np.int8).view(np.int8))

        comp_data[address[n1]] = diff[n1].view(np.int8)

        b2 = [np.array([s]).view(np.int8) for s in diff[n2].astype(np.int16)]

        for i in range(0, len(n2[0])):
            start = int(address[n2[0][i]])
            comp_data[start:start + 2] = b2[i]

        b4 = [np.array([s]).view(np.int8) for s in diff[n4]]

        for i in range(0, len(n4[0])):
            start = int(address[n4[0][i]])
            comp_data[start:start + 4] = b4[i]

        comp_data[0:(nx + 1) * 4] = first_row

        LUT = np.zeros(n_LUT, dtype=np.uint8)

        for i in range(0, 4):
            LUT = np.bitwise_or(np.left_shift(
                lut_vals[slice(i, None, 4)], 2 * i), LUT)
        pass

        return comp_data, LUT

    @classmethod
    def read_histogram(cls, fid):
        hist = {}
        hist = dict()
        hist['hist_NumberOfBins'] = struct.unpack('<i', fid.read(4))[0]
        hist['hist_Value'] = struct.unpack('<%ii' % hist['hist_NumberOfBins'],
                                           fid.read(4 * hist['hist_NumberOfBins']))
        return hist

    @classmethod
    def test_get_long_header(cls, fid):
        nTags = struct.unpack('<i', fid.read(4))[0]

        lh = {}

        for i in range(0, nTags):
            taglen = struct.unpack('<i', fid.read(4))[0]
            tag = struct.unpack('<%is' % taglen, fid.read(taglen))[0]
            tagtype = struct.unpack('<i', fid.read(4))[0]

            if tagtype == 0:
                value = struct.unpack('<i', fid.read(4))[0]

            elif tagtype == 1:
                value = struct.unpack('<d', fid.read(8))[0]

            elif tagtype == 2:

                nlen = int(struct.unpack('<i', fid.read(4))[0])
                value = struct.unpack('<%is' % nlen, fid.read(nlen))[0]

            elif tagtype == 4:
                nlen = int(struct.unpack('<i', fid.read(4))[0])

                n_doub = int(nlen/8)

                value = struct.unpack('<%id' % n_doub, fid.read(nlen))

                # fid.write(struct.pack('<%id' % len(value), *value))
            elif tagtype == 5:
                nlen = int(struct.unpack('<i', fid.read(4))[0])
                value = struct.unpack('<%is' % nlen, fid.read(nlen))[0]
                # fid.write(struct.pack('<i', nlen))
                # fid.write(struct.pack('<%iB' % nlen, *value))

            lh[tag] = (taglen, tagtype, value)

        return lh

    @classmethod
    def write_meta_data(cls, fid, tag, value, taglen, tagtype):

        fid.write(struct.pack('<i', taglen))
        fid.write(struct.pack('<%ss' % taglen, tag))
        fid.write(struct.pack('<i', tagtype))

        if tagtype == 0:
            fid.write(struct.pack('<i', value))
        elif tagtype == 1:
            fid.write(struct.pack('<d', value))
        elif tagtype == 2:
            nlen = len(value)
            fid.write(struct.pack('<i', nlen))
            fid.write(struct.pack('<%is' % nlen, value))
        elif tagtype == 4:

            nlen = len(value) * 8

            fid.write(struct.pack('<i', nlen))

            fid.write(struct.pack('<%id' % len(value), *value))
        elif tagtype == 5:
            nlen = len(value)

            fid.write(struct.pack('<i', nlen))
            fid.write(struct.pack('<%is' % nlen, value))

    def __str__(self):
        toRet = ""
        for key, val in self.header.items():
            toRet += "%s : %s\n" % (key, val)
        return toRet

    def plot(self, ax):
        ax.imshow(self.pixel_data, origin='lower')


if __name__ == '__main__':
    main()
