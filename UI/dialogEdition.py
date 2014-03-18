#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, QtCore, Qt
from edition_UI import Ui_Dialog
from popeye.utils.qimage2ndarray import toqimage
import skimage.io as io


class EditionScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(EditionScene, self).__init__(parent)

    def wheelEvent(self, event):
        """This one is for zoom"""
        pass

class Landmark(QtGui.QGraphicsEllipseItem):

    def __init__(self, nro_landmark, x, y, width=25, height=25, scene=None):
        QtGui.QGraphicsEllipseItem.__init__(self, x, y, width, height, scene=scene)
        self.nro_landmark = nro_landmark
        self.setBrush(QtGui.QColor(0, 0, 0))
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable)

class DialogEdition(QtGui.QDialog):

    def __init__(self, image_path, pos_landmarks, number_landmarks, parent=None):
        """pos_landmarks has the (x,y) of the landmarks
        and number_landmarks are de id landmarks selected"""
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI(image_path, pos_landmarks, number_landmarks)

    def initUI(self, image_path, pos_landmarks, number_landmarks):
        self.ui.graphicsView.scale(0.3, 0.3)
        self.ui.scene = EditionScene()
        self.ui.scene.setSceneRect(QtCore.QRectF())
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        self.load_image(image_path)
        self.load_landmarks(pos_landmarks, number_landmarks)
        
        self.setWindowTitle('Manual Landmarking Edition')
        self.exec_()

    def load_image(self, image_path):
        """Load Image in graphics view of dialog"""
        qitmp = toqimage(io.imread(image_path))
        pix = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp)), scene=self.ui.scene)

    def load_landmarks(self, pos_landmarks, number_landmarks):
        """Set pixmap items in landmarks position and set"""
        for n in number_landmarks:
            Landmark(n, pos_landmarks[n][0], pos_landmarks[n][1], 25, 25, scene=self.ui.scene)
    
    def get_new_landmarks(self):
        landmarks = filter(lambda x: isinstance(x, Landmark), self.ui.scene.items())
        new_landmarks = {}
        for l in landmarks:
            new_landmarks[l.nro_landmark] = [int(l.rect().x()), int(l.rect().y())]
            print new_landmarks[l.nro_landmark]
        return new_landmarks
