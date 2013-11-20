#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import numpy as np

class SaveFile():
	def __init__(self, fileName, landmarks):
		print fileName
		self.name, self.ext = os.path.splitext(fileName)
		self.landmarks = landmarks

	def saveXLS(self):
		pass

	def saveTXT(self):
		pass

	def saveCVS(self):
		pass

	def saveMorphoJ(self):
		pass

	def save(self):
		if self.ext == ".xls":
			self.saveXLS()
		elif self.ext == ".txt":
			self.saveTXT()





