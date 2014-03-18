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
        """ """
        print event.orientation()

class Landmark(QtGui.QGraphicsPixmapItem):
    pass

class DialogEdition(QtGui.QDialog):

    def __init__(self, image_path, pos_landmarks, parent=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI(image_path, pos_landmarks)

    def initUI(self, image_path, pos_landmarks):
        self.ui.scene = EditionScene()
        self.ui.scene.setSceneRect(QtCore.QRectF())
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        self.load_image(image_path)
        self.load_landmarks(pos_landmarks)

        self.setWindowTitle('Manual Landmarking Edition')
        self.exec_()

    def load_image(self, image_path):
        """Load Image in graphics view of dialog"""
        qitmp = toqimage(io.imread(image_path))
        pix = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp)), scene=self.ui.scene)

    def load_landmarks(self, pos_landmarks):
        """Set pixmap items in landmarks position and set"""
        for p in pos_landmarks:
            ell = QtGui.QGraphicsEllipseItem(p[0], p[1], 15, 15, scene=self.ui.scene)
            ell.setBrush(QtGui.QColor(0, 0, 0))