#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Landmark(QtGui.QGraphicsEllipseItem):
    """Black circle with id of landmark location"""
    
    def __init__(self, nro_landmark, x, y, width=25, height=25, scene=None, flag=QtGui.QGraphicsItem.ItemIsMovable, text=False):
        QtGui.QGraphicsEllipseItem.__init__(self, x, y, width, height, scene=scene)
        self.nro_landmark = nro_landmark
        self.setBrush(QtGui.QColor(0, 0, 0))
        self.setFlags(flag)
        if text:
        	self.add_text(x, y, str(nro_landmark), scene)

    def add_text(self, x, y, text, scene):
    	font = QtGui.QFont("Calibri", pointSize=35)
    	txt = QtGui.QGraphicsTextItem(text, scene=scene)
    	txt.setPos(x + 20, y + 20)
    	txt.setFont(font)


