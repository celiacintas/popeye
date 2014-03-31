#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Landmark(QtGui.QGraphicsEllipseItem):
    """Black circle with id of landmark location"""
    
    def __init__(self, nro_landmark, x, y, width=25, height=25, scene=None, flag=QtGui.QGraphicsItem.ItemIsMovable):
        QtGui.QGraphicsEllipseItem.__init__(self, x, y, width, height, scene=scene)
        self.nro_landmark = nro_landmark
        self.setBrush(QtGui.QColor(0, 0, 0))
        self.setFlags(flag)
        self.add_text(x, y, str(nro_landmark), scene)

    def add_text(self, x, y, text, scene):
    	t = QtGui.QGraphicsTextItem(text, scene=scene)
    	t.setPos(x + 20, y + 20)

