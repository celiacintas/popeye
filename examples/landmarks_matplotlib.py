#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""In this example we can see how to call 
the s_search_single fuction of STASM from Python """

import os
import matplotlib.pyplot as plt
from ..dependencies import pystasm
import skimage.io as io
from skimage.draw import circle



FILENAME = os.path.join(os.path.dirname(__file__), "../Tests/Data/test.jpg")


def main():
    mystasm = pystasm.STASM()
    mylandmarks = mystasm.s_search_single(FILENAME)
    image = io.imread(FILENAME)
    for i in range(len(mylandmarks)):
        radio, center = circle(mylandmarks[i][1], mylandmarks[i][0], 15)
        image[radio, center] = 1
    io.imshow(image)
    plt.show()

if __name__ == '__main__':
    main()
