#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import numpy as np
 
def toQImage(im):
    if im is None:
        return QImage()
    elif len(im.shape) == 3:
        if im.shape[2] == 3:
            qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_RGB888);
            return qim
        elif im.shape[2] == 4:
            qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_ARGB32);
            return qim