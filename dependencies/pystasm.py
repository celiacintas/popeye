#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ctypes implementation for STASM library
# http://www.milbo.users.sonic.net/stasm/

import ctypes
import numpy as np
import skimage.io as io
from skimage import img_as_ubyte
import os
import logging

F = os.path.dirname(__file__)
FILENAMESTASM = os.path.join(F, "stasm/libstasm.so")
FILENAMEDATA = os.path.join(F, "Data")


class STASM(object):
    """This is a Python wrapper for the STASM library"""

    def __init__(self):
        """Loads de .so file """
        self.stasm = ctypes.cdll.LoadLibrary(FILENAMESTASM)

    def s_init(self, path2data=FILENAMEDATA, debug=0):
        """Gives the location of the Haar Cascade files"""
        self.stasm.stasm_init(path2data, debug)

    def s_search_single(self, filename, numberlandmarks=77,
                        path2data=FILENAMEDATA):
        """Search face and landmarks in picture"""
        try:
            image = img_as_ubyte(io.imread(filename, as_grey=True))
            
        except IOError, exc:
            logging.error(exc.message, exc_info=True)
            raise IOError

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
        xys = 2 * numberlandmarks
        landmarks = (ctypes.c_float * xys)()

        self.stasm.stasm_search_single(ctypes.byref(foundface), landmarks,
            image.ctypes.data_as(ctypes.POINTER(ctypes.c_char)),
            ctypes.c_int(image.shape[1]), ctypes.c_int(image.shape[0]),
            filename, FILENAMEDATA)
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
        """Force landmarks into image boundary"""
        pass

    def s_convert_shape(self):
        """Convert stasm 77 to 77=nochange
        76=stasm3 68=xm2vts 22=ar 20=bioid 17=me17"""
        pass

#-----------------------------------------------------------------


def main():
    #home made test TODO make unitttest
    mystasm = STASM()
    mystasm.s_init()
    landmarks_found = mystasm.s_search_single("test.JPG")
    print landmarks_found

if __name__ == '__main__':
    main()
