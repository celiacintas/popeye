#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import os
from PyQt4 import QtCore, QtGui
from popeye.UI.popEye_UI import Ui_MainWindow
from popeye.UI.myScene import Scene
from popeye.UI.table import Table
from popeye.UI.myButton import MyButton
from popeye.UI.pixmapItem import PixmapItem
from ..utils.qimage2ndarray import toqimage
from popeye.UI.states import (StateInit, StateImageLoading,
                                     StateLanmarkingSelection,
                                     StateSaveLandmarking,
                                     StateClear, StateExit,
                                     StateAbout, StateRunLandmarking,
                                     StateInitRun, StateFoward,
                                     StateBack, StateEdit)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = QtCore.QSettings()
        self.settings.setValue("last_dir", os.getcwd())
        filename = os.path.dirname(__file__)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(
            QtGui.QPixmap(os.path.join(filename, "Images/back.png")))
        palette.setBrush(QtGui.QPalette.Background, brush)
        self.setPalette(palette)
        self.ui.scene = Scene()
        self.ui.scene.setSceneRect(0, 0, 700, 300)
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        #self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        self.ui.myButtonNext = MyButton(
            os.path.join(filename, "Icons/next.png"), "Next ..", False)
        self.ui.myButtonPrev = MyButton(
            os.path.join(filename, "Icons/prev.png"), "Prev ..", False)
        self.ui.myButtonEdit = MyButton(
            os.path.join(filename, "Icons/learn.png"), "Edit ..", False)
        self.ui.scene.buttonsForChecker(
            self.ui.myButtonNext, self.ui.myButtonEdit,
            self.ui.myButtonPrev)
        self.ui.graphicsView.show()

        self.landn = 77
        self.count = None
        self.create_machine()

    def create_machine(self):
        self.machine = QtCore.QStateMachine()
        self.create_states()
        self.create_transitions()
        self.machine.setInitialState(self.init)
        self.machine.start()

    def create_states(self):
        """Generate states of the SM according to
        the  behavior of the GUI"""
        # States
        self.init = StateInit(self.machine, self.ui)
        self.image_load = StateImageLoading(self.machine, self)
        self.landmarking_selection = StateLanmarkingSelection(
            self.machine, self)
        self.save = StateSaveLandmarking(self.machine, self)
        self.clear = StateClear(self.machine, self)
        self.quit = StateExit(self.machine, self)
        self.about = StateAbout(self.machine, self)
        self.run = StateRunLandmarking(self.machine, self)

        # Group of states for run
        self.run_init = StateInitRun(self.run, self)
        self.run_fwd = StateFoward(self.run, self)
        self.run_bck = StateBack(self.run, self)
        self.run_edit = StateEdit(self.run, self)
        self.run.setInitialState(self.run_init)

    def create_transitions(self):
        """Assign the trasintion to the SM according to
        the  behavior of the GUI"""
        # Transitions
        self.init.addTransition(self.ui.pushButton.clicked, self.image_load)
        self.init.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.init.addTransition(self.ui.pushButton_6.clicked, self.about)

        self.image_load.addTransition(
            self.ui.pushButton_2.clicked, self.landmarking_selection)
        self.image_load.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.image_load.addTransition(self.ui.pushButton.clicked, self.clear)
        self.image_load.addTransition(self.ui.pushButton_6.clicked, self.about)

        self.landmarking_selection.addTransition(
            self.ui.pushButton_2.clicked, self.landmarking_selection)
        self.landmarking_selection.addTransition(
            self.ui.pushButton_3.clicked, self.run)
        self.landmarking_selection.addTransition(
            self.ui.pushButton_5.clicked, self.quit)
        self.landmarking_selection.addTransition(
            self.ui.pushButton_6.clicked, self.about)
        self.save.addTransition(self.ui.pushButton_4.clicked, self.save)
        self.save.addTransition(
            self.ui.pushButton_2.clicked, self.landmarking_selection)
        self.save.addTransition(self.ui.pushButton.clicked, self.clear)
        self.save.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.save.addTransition(self.ui.pushButton_6.clicked, self.about)
        self.save.addTransition(self.ui.pushButton_3.clicked, self.run)

        self.clear.addTransition(self.clear.finished, self.image_load)

        self.about.addTransition(self.ui.pushButton.clicked, self.clear)
        self.about.addTransition(
            self.ui.pushButton_2.clicked, self.landmarking_selection)
        self.about.addTransition(self.ui.pushButton_3.clicked, self.run)
        self.about.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.about.addTransition(self.ui.pushButton_6.clicked, self.about)
        self.about.addTransition(self.ui.pushButton_4.clicked, self.save)

        self.quit.addTransition(self.ui.pushButton.clicked, self.clear)
        self.quit.addTransition(
            self.ui.pushButton_2.clicked, self.landmarking_selection)
        self.quit.addTransition(self.ui.pushButton_3.clicked, self.run)
        self.quit.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.quit.addTransition(self.ui.pushButton_6.clicked, self.about)
        self.quit.addTransition(self.ui.pushButton_4.clicked, self.save)

        self.run.addTransition(self.ui.pushButton.clicked, self.clear)
        self.run.addTransition(
            self.ui.pushButton_2.clicked, self.landmarking_selection)
        self.run.addTransition(self.ui.pushButton_3.clicked, self.run)
        self.run.addTransition(self.ui.pushButton_4.clicked, self.save)
        self.run.addTransition(self.ui.pushButton_5.clicked, self.quit)
        self.run.addTransition(self.ui.pushButton_6.clicked, self.about)
        # Transitions under run
        self.run_init.addTransition(self.ui.myButtonPrev.clicked, self.run_bck)
        self.run_init.addTransition(self.ui.myButtonEdit.clicked, self.run_edit)
        self.run_init.addTransition(self.ui.myButtonNext.clicked, self.run_fwd)

        self.run_fwd.addTransition(self.ui.myButtonPrev.clicked, self.run_bck)
        self.run_fwd.addTransition(self.ui.myButtonNext.clicked, self.run_fwd)
        self.run_fwd.addTransition(self.ui.myButtonEdit.clicked, self.run_edit)

        self.run_bck.addTransition(self.ui.myButtonPrev.clicked, self.run_bck)
        self.run_bck.addTransition(self.ui.myButtonNext.clicked, self.run_fwd)
        self.run_bck.addTransition(self.ui.myButtonEdit.clicked, self.run_edit)

    def draw_landmarks(self):
        """Put the landmarked images in the scene and load a table
        with the (nl, x, y)"""
        # TODO remove this fuction .. translate to new state
        mytable = Table(self.numberOfLandmarks, ['x', 'y'])
        mylandmarks = self.myfinder.landmarks[self.count]
        myfilterlandmarks = [mylandmarks[i]
                             for i in self.numberOfLandmarks]
        load_model(myfilterlandmarks, mytable)
        proxytabla = QtGui.QGraphicsProxyWidget()
        proxytabla.setWidget(mytable)
        proxytabla.setPos(320, 0)

        qitmp = toqimage(self.images[self.count])
        pix = QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp))
        PixmapItem(pix.scaledToWidth(310), None, self.ui.scene)
        self.ui.scene.addItem(proxytabla)

def load_model(landmarks, mytable):
    mymodel = mytable.model()
    for i in range(len(landmarks)):
        for j in range(len(landmarks[0])):
            mymodel[i, j] = float(landmarks[i][j])
