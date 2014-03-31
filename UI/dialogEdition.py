#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, QtCore, Qt
from edition_UI import Ui_Dialog
from popeye.utils.qimage2ndarray import toqimage
import skimage.io as io
from landmark import Landmark

class DialogEdition(QtGui.QDialog):
    """Dialog for manual fix of landmark x,y position"""

    def __init__(self, image_path, pos_landmarks, number_landmarks, parent=None):
        """pos_landmarks has the (x,y) of the landmarks
        and number_landmarks are de id landmarks selected"""
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI(image_path, pos_landmarks, number_landmarks)

    def initUI(self, image_path, pos_landmarks, number_landmarks):
        """Create scene and put image and landmarks visible."""
        self.ui.graphicsView.scale(0.3, 0.3)
        self.ui.scene = QtGui.QGraphicsScene()
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
        """Set the new position of the manual landmarking, passing the points of scene 
        to real ones.."""
        landmarks = filter(lambda x: isinstance(x, Landmark), self.ui.scene.items())
        new_landmarks = {}
        for l in landmarks:
            new_landmarks[l.nro_landmark] = [int(l.rect().x() + l.scenePos().x() ), int(l.rect().y() + l.scenePos().y())]
        return new_landmarks
