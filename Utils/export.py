#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from os.path import basename
import numpy as np


class SaveFile():

    def __init__(self, imagesNames, fileName, landmarks, filterLandmarks):
        """
        Detect extension of file and filter landmarks to save
        """
        self.name, self.ext = os.path.splitext(fileName)
        self.landmarks = landmarks
        self.filterLandmarks = [[l[i] for i in filterLandmarks]
                                for l in landmarks]
        self.nfilter = len(filterLandmarks)
        self.idCodes = map(lambda p: os.path.splitext(basename(p))[0],
                           imagesNames)

    def saveXLS(self, out):
        pass

    def saveTXT(self, out):
        # TODO add code name of the ind
        map(lambda x: np.savetxt(out, x, fmt='%i %i'), self.filterLandmarks)

    def saveCVS(self, out):

        pass

    def saveMorphoJ(self, out):
        for id in range(len(self.idCodes)):
            out.write("".join([self.idCodes[id], ' ']))
            np.savetxt(out, np.array(self.filterLandmarks[id]).reshape(
                1, len(self.filterLandmarks[id]) * 2),  fmt='%i')
            # Change the shape for MorphoJ All landmarks in one line per person

    def saveTPS(self, out):
        """
        Save the chosen landmarks in TPS format
        http://life.bio.sunysb.edu/morph/soft-tps.html
        """
        for l in range(len(self.filterLandmarks)):
            out.write(str(self.nfilter).join(["LM=", '\n']))
            map(lambda x: np.savetxt(out, self.filterLandmarks[l][x].reshape(
                (1, 2)), fmt='%i %i'), [i for i in range(self.nfilter)])
            out.write(str(l).join(["ID=", '\n']))

    def save(self):
        with open(''.join([self.name, self.ext]), 'w') as out:
            if self.ext == ".xls":
                self.saveXLS(out)
            elif self.ext == ".tps":
                self.saveTPS(out)
            elif self.ext == ".txt":
                self.saveMorphoJ(out)
            out.close()
