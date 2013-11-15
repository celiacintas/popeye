#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import pystasm

class Finder():
	def __init__(self, pathFile):
		self.fileNames = [os.path.join(pathFile,f) for f in os.listdir(pathFile) if re.match(r'.*\.JPG', f)]
		self.myStasm = pystasm.STASM()

	def findFace(self):
		pass

	def findLandmarks(self, numberLandmarks=77):
		return map(self.myStasm.s_search_single, self.fileNames)


def main():
	myFinder = Finder("/home/celia/Test/")
	landmarks = myFinder.findLandmarks()
	print landmarks


if __name__ == '__main__':
	main()
