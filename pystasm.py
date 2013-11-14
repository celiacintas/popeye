#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ctypes
import numpy as np
import cv2
import matplotlib.pyplot as plt

class STASM:
	def __init__(self, fileName):
		self.stasm = ctypes.cdll.LoadLibrary("Dependencies/libstasm.so")
		self.image = cv2.imread(fileName, cv2.CV_LOAD_IMAGE_GRAYSCALE)

	def s_init(self, pathToData="Dependencies/Data", debug = 0):
		self.stasm.stasm_init( pathToData, debug)

	def s_search_single(self, filename, numberLandmarks=77, pathToData="Dependencies/Data"):
		self.stasm.stasm_search_single.restypes = [ctypes.c_int]
		self.stasm.stasm_search_single.argtypes = [ctypes.POINTER(ctypes.c_int), 
												   ctypes.POINTER(ctypes.c_float),
												   ctypes.POINTER(ctypes.c_char),
												   ctypes.c_int,
												   ctypes.c_int,
												   ctypes.POINTER(ctypes.c_char),
												   ctypes.POINTER(ctypes.c_char),
												   ]
		foundface = ctypes.c_int()
		pointer_foundface = ctypes.pointer(foundface)
		xys = 2*numberLandmarks
		landmarks = (ctypes.c_float*xys)()
		
		test = self.stasm.stasm_search_single(ctypes.byref(foundface), landmarks,
		self.image.ctypes.data_as(ctypes.POINTER(ctypes.c_char)),
		ctypes.c_int(self.image.shape[1]), ctypes.c_int(self.image.shape[0]),
		filename, "Dependencies/Data")
		points = np.array(list(landmarks)).reshape((77,2))
		print points

	def s_open_image(self):
		pass

	def s_search_auto(self):
		pass

	def s_search_pinned(self):
		pass

	def s_stasm_lasterr(self):
		pass

	def s_force_points_into_image(self):
		pass

	def s_convert_shape(self):
		pass

#-----------------------------------------------------------------
def main():
	myStasm = STASM("/home/celia/Chile/test.JPG")
	myStasm.s_init()
	myStasm.s_search_single("/home/celia/Chile/test.JPG")

if __name__ == '__main__':
	main()