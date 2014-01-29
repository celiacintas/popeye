#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import popeyeReloaded.Dependencies.pystasm as pystasm
import skimage.io as io
from skimage.draw import circle
import numpy as np


class Finder(object):
    """
    Finder is in charge of loading the image and pass it
    to pystasm to return the landmarks position
    """

    def __init__(self, pathfile):
        """
        Create de Stasm module and save the files names.
        """
        #self.fileNames = [os.path.join(pathFile,f) for
        #f in os.listdir(pathFile) if re.match(r'.*\.JPG', f)]
        self.filenames = pathfile
        self.mystasm = pystasm.STASM()
        self.landmarks = None

    def find_face(self):
        """return ok if face found"""
        #TODO implement this
        pass

    def find_landmarks(self):
        """
        Get all the landmarks of the selected images.
        """
        self.landmarks = np.array(
            [self.mystasm.s_search_single(name) for name in self.filenames])

    def draw_landmarks(self, pos_landmarks):
        """
        Draw the selected landmarks and return the modified image.
        """
        images = [io.imread(f) for f in self.filenames]
        for i in range(len(images)):
            for j in pos_landmarks:
                radio, center = circle(
                    self.landmarks[i][j][1], self.landmarks[i][j][0], 15)
                images[i][radio, center] = 1
        return images


def main():
    """
    Home made test #TODO pass to unittest
    """
    myfinder = Finder(["test.JPG"])
    myfinder.find_landmarks()
    myfinder.draw_landmarks([i for i in range(77)])

if __name__ == '__main__':
    main()
