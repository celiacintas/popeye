#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QImage, qRgb
import numpy as np
 
gray_color_table = [qRgb(i, i, i) for i in range(256)]
 
def toQImage(im):
    if im is None:
        return QImage()
 
    if im.dtype == np.uint8:
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim
 
        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                return qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                return qim