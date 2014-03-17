#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, QtCore
from edition_UI import Ui_Dialog
from popeye.utils.qimage2ndarray import toqimage

class DialogEdition(QtGui.QDialog):

    def __init__(self, image, pos_landmarks, parent=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI(image, pos_landmarks)

    def initUI(self, image, pos_landmarks):
        self.ui.scene = QtGui.QGraphicsScene()
        self.ui.scene.setSceneRect(QtCore.QRectF())
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        qitmp = toqimage(image)
        pix = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp)), scene=self.ui.scene)

        self.setWindowTitle('Manual Landmarking Edition')
        self.exec_()
