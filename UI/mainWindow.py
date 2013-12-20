#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import os
import sys
from finder import Finder
from PyQt4 import QtCore, QtGui
from UI.popEye_UI import Ui_MainWindow
from UI.myScene import Scene
from UI.table import Table
from Utils.qimage2ndarray import toQImage
from states import *


class Main_Window(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.scene = Scene()
        self.ui.scene.setSceneRect(0, 0, 700, 300)
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        self.ui.actionAbout.triggered.connect(self.showAbout)
        self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.ui.pushButton_6.clicked.connect(self.showAbout)
        self.ui.pushButton_5.clicked.connect(self.showQuit)

        self.ui.graphicsView.show()
        self.photosNames = list()
        self.landn = 77
        self.machine = QtCore.QStateMachine()

        # States
        self.state1 = State_Init(self.machine, self.ui)
        self.state2 = State_ImageLoading(self.machine, self)
        self.state3 = State_LanmarkingSelection(self.machine, self)
        self.state4 = State_runLandmarking(self.machine, self)
        self.state5 = State_saveLandmarking(self.machine, self)

        # Transitions
        self.state1.addTransition(self.ui.pushButton.clicked, self.state2)
        self.state2.addTransition(self.ui.pushButton_2.clicked, self.state3)
        #TODO primero un clean
        self.state2.addTransition(self.ui.pushButton.clicked, self.state2)
        self.state3.addTransition(self.ui.pushButton_2.clicked, self.state3)
        self.state3.addTransition(self.ui.pushButton_3.clicked, self.state4)
        self.state4.addTransition(self.ui.pushButton_2.clicked, self.state3)

        self.state4.addTransition(self.ui.pushButton_3.clicked, self.state4)
        self.state4.addTransition(self.ui.pushButton_4.clicked, self.state5)
        self.state5.addTransition(self.ui.pushButton_4.clicked, self.state5)
        self.state5.addTransition(self.ui.pushButton_2.clicked, self.state3)

        self.machine.setInitialState(self.state1)
        self.machine.start()

    def showQuit(self):
        """Exit dialog."""
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Do you really want to go??", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    def showAbout(self):
        """Credits."""
        text = u"""<font color=black> PopEye is made in Python and C++ using several libraries such as:  
        numpy, scikit-image, STASM (with ctypes), scikit-learn.
        All the develop is made by people of GIBEH, CENPAT-CONICET.<br></font>
        """
        return QtGui.QMessageBox.about(self, u"About PopEye", text)

    def removeFromScene(self):
        # TODO make an state
        items = self.ui.scene.items()
        for i in items:
            #if isinstance(i, QtGui.QGraphicsProxyWidget):
            #    i.setVisible(False)
            if isinstance(i, PixmapItem) and not i.isVisible():
                self.photosNames.remove(i.path)
            #if not isinstance(i, QtGui.QGraphicsProxyWidget):
            #    self.ui.scene.removeItem(i)

    # prev next and save to one small FA
    def prev(self):
        if 0 < self.count < len(self.images):
            self.count = self.count - 1
            self.drawLandmarks()
        else:
            self.ui.myButtonPrev.setEnabled(False)
        if not self.ui.myButtonNext.isEnabled():
            self.ui.myButtonNext.setEnabled(True)

    def next(self):
        if 0 <= self.count < len(self.images) - 1:
            self.count = self.count + 1
            self.drawLandmarks()
        else:
            self.ui.myButtonNext.setEnabled(False)
        if not self.ui.myButtonPrev.isEnabled():
            self.ui.myButtonPrev.setEnabled(True)

    def drawLandmarks(self):
            self.myTable = Table(self.numberOfLandmarks, ['x', 'y'])
            myLandmarks = self.myFinder.landmarks[self.count]
            myFilterLandmarks = [myLandmarks[i]
                                 for i in self.numberOfLandmarks]
            self.loadModel(myFilterLandmarks)
            proxyTabla = QtGui.QGraphicsProxyWidget()
            proxyTabla.setWidget(self.myTable)
            proxyTabla.setPos(320, 0)

            qitmp = toQImage(self.images[self.count])
            pix = QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp))
            sca = PixmapItem(pix.scaledToWidth(310), None)
            self.ui.scene.addItem(sca)
            self.ui.scene.addItem(proxyTabla)

    def loadModel(self, landmarks):
        myModel = self.myTable.model()
        for i in range(len(landmarks)):
            for j in range(len(landmarks[0])):
                myModel[i, j] = float(landmarks[i][j])

    def edit(self):
        pass

    