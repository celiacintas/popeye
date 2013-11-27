#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import numpy as np

class SaveFile():
	def __init__(self, fileName, landmarks, filterLandmarks):
		self.name, self.ext = os.path.splitext(fileName)
		self.landmarks = landmarks
		#self.filterLandmarks = [[l[i].tolist() for i in filterLandmarks] for l in landmarks]
		self.filterLandmarks = [[l[i] for i in filterLandmarks] for l in landmarks]
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
		with open(self.name + self.ext, 'w') as out:
			for l in range(len(self.filterLandmarks)):
				out.write(str("LM=" + str(self.nfilter) + '\n'))
				map(lambda x: np.savetxt(out, self.filterLandmarks[l][x].reshape((1,2)), fmt='%i %i'), [i  for i in range(self.nfilter)])
				out.write(str("ID="+str(l)+'\n'))
			out.close()

	def save(self):
		if self.ext == ".xls":
			self.saveXLS()
		elif self.ext == ".tps":
			self.saveTPS()





