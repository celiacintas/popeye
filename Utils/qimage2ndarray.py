#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QImage

def toqimage(image):
    if image is None:
        return QImage()
    elif len(image.shape) == 3:
        if image.shape[2] == 3:
            qim = QImage(image.data, image.shape[1],
            	  image.shape[0], image.strides[0], QImage.Format_RGB888)
            return qim
        elif image.shape[2] == 4:
            qim = QImage(image.data, image.shape[1],
            	  image.shape[0], image.strides[0], QImage.Format_ARGB32)
            return qim
