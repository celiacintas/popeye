#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import numpy as np


class SaveFile():

    def __init__(self, fileName, landmarks, filterLandmarks):
        """
        Detect extension of file and filter landmarks to save
        """
        self.name, self.ext = os.path.splitext(fileName)
        self.landmarks = landmarks
        self.filterLandmarks = [[l[i] for i in filterLandmarks]
                                for l in landmarks]
        self.nfilter = len(filterLandmarks)

    def saveXLS(self):
        pass

    def saveTXT(self):
        pass

    def saveCVS(self):
        pass

    def saveMorphoJ(self):
        pass

    def saveTPS(self):
        """
        Save the chosen landmarks in TPS format
        http://life.bio.sunysb.edu/morph/soft-tps.html
        """
        with open(''.join([self.name, self.ext]), 'w') as out:
            for l in range(len(self.filterLandmarks)):
                out.write(str(self.nfilter).join(["LM=", '\n']))
                map(lambda x: np.savetxt(out, self.filterLandmarks[l][x].reshape(
                    (1, 2)), fmt='%i %i'), [i for i in range(self.nfilter)])
                out.write(str(l).join(["ID=", '\n']))
            out.close()

    def save(self):
        if self.ext == ".xls":
            self.saveXLS()
        elif self.ext == ".tps":
            self.saveTPS()
        elif self.ext == ".txt":
            self.saveTXT()
