#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from os.path import basename
import numpy as np
import logging

class NoExtensionKnowException(Exception):
    """Exception for no images loaded"""

    def __init__(self):
        Exception.__init__(self, "Unknown file extension")

class SaveFile(object):

    """This class is in charge of save in diferent formats
    the landmarks obtained from the image (id, x, y, number of landmarks)"""

    def __init__(self, imagesnames, filename, landmarks, filterlandmarks):
        """
        Detect extension of file and filter landmarks to save
        """
        self.name, self.ext = os.path.splitext(filename)
        self.landmarks = landmarks
        self.filterlandmarks = [[l[i] for i in filterlandmarks]
                                for l in landmarks]
        self.nfilter = len(filterlandmarks)
        self.idcodes = map(lambda p:os.path.splitext(basename(p))[0], imagesnames)

    def savexls(self, out):
        """Save landmarks in spreadsheet"""
        pass

    def savetxt(self, out):
        """Save landmarks in txt (x, y)"""
        # TODO add code name of the ind
        map(lambda x: np.savetxt(out, x, fmt='%i %i'), self.filterlandmarks)

    def savecvs(self, out):
        """Save landmarks in cvs (x, y)"""
        pass

    def savemorphoj(self, out):
        """Save landmarks in txt whit morphoJ format
        id (x y x y x y)*numberLandmarks"""
        for i in range(len(self.idcodes)):
            out.write("".join([self.idcodes[i], ' ']))
            np.savetxt(out, np.array(self.filterlandmarks[i]).reshape(
                1, len(self.filterlandmarks[i]) * 2), fmt='%i')
            # Change the shape for MorphoJ All landmarks in one line per person

    def savetps(self, out):
        """
        Save the chosen landmarks in TPS format
        http://life.bio.sunysb.edu/morph/soft-tps.html
        LM=numberLandmarks
        x y
        x y
        ...
        ...
        id=numberId
        """
        for landmark in range(len(self.filterlandmarks)):
            out.write(str(self.nfilter).join(["LM=", '\n']))
            map(lambda x: np.savetxt(out,
                self.filterlandmarks[landmark][x].reshape((1, 2)),
                fmt='%i %i'), [i for i in range(self.nfilter)])
            out.write(str(landmark).join(["ID=", '\n']))

    def save(self):
        """Dependending on the extension file name .. the save
        that we want to call"""
        with open(''.join([self.name, self.ext]), 'w') as out:
            try:
                if self.ext == ".xls":
                    self.savexls(out)
                elif self.ext == ".tps":
                    self.savetps(out)
                elif self.ext == ".txt":
                    self.savemorphoj(out)
                else:
                    raise NoExtensionKnowException
                out.close()
                            
            except NoExtensionKnowException, exc:
                logging.error(exc.message, exc_info=True)
                raise
