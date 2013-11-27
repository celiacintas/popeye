#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import pystasm
import skimage.io as io
from skimage.draw import circle
from skimage import img_as_ubyte
import numpy as np

class Finder():
	def __init__(self, pathFile):
		#self.fileNames = [os.path.join(pathFile,f) for f in os.listdir(pathFile) if re.match(r'.*\.JPG', f)]
		self.fileNames = pathFile
		self.myStasm = pystasm.STASM()

	def findFace(self):
		pass

	def findLandmarks(self, numberLandmarks=77):
		self.landmarks = np.array(map(self.myStasm.s_search_single, self.fileNames))


	def drawLandmarks(self, posLandmarks):
		images = map(lambda f: (io.imread(f)), self.fileNames)
		for i in range(len(images)):
			for l in posLandmarks:
				rr, cc = circle(self.landmarks[i][l][1], self.landmarks[i][l][0], 15)
				images[i][rr, cc] = 1
		return images

def main():
	myFinder = Finder(["/home/celia/Chile/test.JPG"])
	myFinder.findLandmarks()
	myFinder.drawLandmarks()
	
if __name__ == '__main__':
	main()
