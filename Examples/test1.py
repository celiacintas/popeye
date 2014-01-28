#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
import sys

#path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#if not path in sys.path:
#    sys.path.insert(1, path)
#del path

import matplotlib.pyplot as plt
from ..Dependencies import pystasm
import skimage.io as io
from skimage.draw import circle
from skimage import img_as_ubyte
import numpy as np



def main():
    FILENAME = "../Tests/Data/test.jpg"

    myStasm = pystasm.STASM()
    myLandmarks = myStasm.s_search_single(FILENAME)
    image = io.imread(FILENAME)
    print myLandmarks
    for i in range(len(myLandmarks)):
        rr, cc = circle(myLandmarks[i][1], myLandmarks[i][0], 15)
        image[rr, cc] = 1
    pepe = io.imshow(image)
    plt.show()

if __name__ == '__main__':
    main()
