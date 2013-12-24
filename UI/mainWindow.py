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
        self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.ui.myButtonNext = MyButton(
            "UI/Icons/next.png", "Next ..", False)
        self.ui.myButtonPrev = MyButton(
            "UI/Icons/prev.png", "Prev ..", False)
        self.ui.myButtonEdit = MyButton(
            "UI/Icons/learn.png", "Edit ..", False)
        self.ui.scene.buttonsForChecker(
            self.ui.myButtonNext, self.ui.myButtonEdit,
            self.ui.myButtonPrev)
        self.ui.graphicsView.show()

        self.landn = 77
        self.machine = QtCore.QStateMachine()

        # States
        self.init = State_Init(self.machine, self.ui)
        self.imageLoad = State_ImageLoading(self.machine, self)
        self.landmarkingSelection = State_LanmarkingSelection(
            self.machine, self)
        self.save = State_saveLandmarking(self.machine, self)
        self.clear = State_clear(self.machine, self)
        self.quit = State_exit(self.machine, self)
        self.about = State_about(self.machine, self)
        self.run = State_runLandmarking(self.machine, self)

        # Group of states for run
        run_init = State_init_run(self.run, self)
        run_fwd = State_foward(self.run, self)
        run_bck = State_back(self.run, self)
        run_edit = State_edit(self.run, self)
        self.run.setInitialState(run_init)

        # Transitions
        self.init.addTransition(self.ui.pushButton.clicked, self.imageLoad)
        self.init.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.init.addTransition(self.ui.pushButton_6.clicked, self.about)

        self.imageLoad.addTransition(
            self.ui.pushButton_2.clicked, self.landmarkingSelection)
        self.imageLoad.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.imageLoad.addTransition(self.ui.pushButton.clicked, self.clear)
        self.imageLoad.addTransition(self.ui.pushButton_6.clicked, self.about)

        self.landmarkingSelection.addTransition(
            self.ui.pushButton_2.clicked, self.landmarkingSelection)
        self.landmarkingSelection.addTransition(
            self.ui.pushButton_3.clicked, self.run)
        self.landmarkingSelection.addTransition(
            self.ui.pushButton_5.clicked, self.quit)
        self.landmarkingSelection.addTransition(
            self.ui.pushButton_6.clicked, self.about)
        self.save.addTransition(self.ui.pushButton_4.clicked, self.save)
        self.save.addTransition(
            self.ui.pushButton_2.clicked, self.landmarkingSelection)
        self.save.addTransition(self.ui.pushButton.clicked, self.clear)
        self.save.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.save.addTransition(self.ui.pushButton_6.clicked, self.about)
        self.save.addTransition(self.ui.pushButton_3.clicked, self.run)

        self.clear.addTransition(self.clear.finished, self.imageLoad)

        self.about.addTransition(self.ui.pushButton.clicked, self.imageLoad)
        self.about.addTransition(
            self.ui.pushButton_2.clicked, self.landmarkingSelection)
        self.about.addTransition(self.ui.pushButton_3.clicked, self.run)
        self.about.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.about.addTransition(self.ui.pushButton_6.clicked, self.about)
        self.about.addTransition(self.ui.pushButton_4.clicked, self.save)

        self.quit.addTransition(self.ui.pushButton.clicked, self.imageLoad)
        self.quit.addTransition(
            self.ui.pushButton_2.clicked, self.landmarkingSelection)
        self.quit.addTransition(self.ui.pushButton_3.clicked, self.run)
        self.quit.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.quit.addTransition(self.ui.pushButton_6.clicked, self.about)
        self.quit.addTransition(self.ui.pushButton_4.clicked, self.save)

        self.run.addTransition(self.ui.pushButton.clicked, self.clear)
        self.run.addTransition(
            self.ui.pushButton_2.clicked, self.landmarkingSelection)
        self.run.addTransition(self.ui.pushButton_3.clicked, self.run)
        self.run.addTransition(self.ui.pushButton_4.clicked, self.save)
        self.run.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.run.addTransition(self.ui.pushButton_6.clicked, self.about)
        # Transitions under run
        run_init.addTransition(self.ui.myButtonNext.clicked, run_fwd)
        run_init.addTransition(self.ui.myButtonPrev.clicked, run_bck)
        run_init.addTransition(self.ui.myButtonEdit.clicked, run_edit)

        self.machine.setInitialState(self.init)
        self.machine.start()

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
            sca = PixmapItem(pix.scaledToWidth(310), None, self.ui.scene)
            self.ui.scene.addItem(proxyTabla)

    def loadModel(self, landmarks):
        myModel = self.myTable.model()
        for i in range(len(landmarks)):
            for j in range(len(landmarks[0])):
                myModel[i, j] = float(landmarks[i][j])

