#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ctypes implementation for STASM library
# http://www.milbo.users.sonic.net/stasm/

import ctypes
import numpy as np
import skimage.io as io
from skimage import img_as_ubyte
import os

dir = os.path.dirname(__file__)
filenameStasm = os.path.join(dir, "stasm/libstasm.so")
filenameData = os.path.join(dir, "Data")


class STASM:

    def __init__(self):
        self.stasm = ctypes.cdll.LoadLibrary(filenameStasm)
        # io.use_plugin('pil')

    def s_init(self, pathToData=filenameData, debug=0):
        self.stasm.stasm_init(pathToData, debug)

    def s_search_single(self, fileName, numberLandmarks=77, pathToData=filenameData):
        image = img_as_ubyte(io.imread(fileName, as_grey=True))

        self.stasm.stasm_search_single.restypes = [ctypes.c_int]
        self.stasm.stasm_search_single.argtypes = [ctypes.POINTER(
            ctypes.c_int),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_char),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_char),
            ctypes.POINTER(ctypes.c_char)]
        foundface = ctypes.c_int()
        pointer_foundface = ctypes.pointer(foundface)
        xys = 2 * numberLandmarks
        landmarks = (ctypes.c_float * xys)()

        test = self.stasm.stasm_search_single(
            ctypes.byref(foundface), landmarks,
            image.ctypes.data_as(ctypes.POINTER(ctypes.c_char)),
            ctypes.c_int(image.shape[1]), ctypes.c_int(image.shape[0]),
            fileName, filenameData)
        points = np.array(list(landmarks)).reshape((77, 2))

        return points

    def s_open_image(self):
        pass

    def s_search_auto(self):
        pass

    def s_search_pinned(self):
        pass

    def s_stasm_lasterr(self):
        pass

    def s_force_points_into_image(self):
        pass

    def s_convert_shape(self):
        pass

#-----------------------------------------------------------------


def main():
    myStasm = STASM()
    myStasm.s_init()
    landmarks_found = myStasm.s_search_single("/home/celia/Chile/test.JPG")
    print landmarks_found

if __name__ == '__main__':
    main()