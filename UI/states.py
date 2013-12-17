#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import os
from PyQt4 import QtCore, QtGui
from UI.pixmapItem import PixmapItem
from UI.dialogOptions import DialogOptions
from UI.myButton import MyButton
from finder import Finder

class State_Init(QtCore.QState):

    def __init__(self, machine, ui):
        QtCore.QState.__init__(self, machine)
        self.ui = ui
 
    def onEntry(self, e):
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)

    def onExit(self, e):
        pass

class State_ImageLoading(QtCore.QState):

    def __init__(self, machine, win):
        QtCore.QState.__init__(self, machine)
        self.window = win

    def onEntry(self, e):
        dialog = QtGui.QFileDialog()
        outFileNames = dialog.getOpenFileNames(self.window, "Open Image",
                                               os.getcwd(),
                                               "Image Files (*.png *.jpg *.bmp)")
        self.drawPeople(outFileNames)
        self.window.photosNames = outFileNames
        self.window.ui.pushButton_2.setEnabled(True)

    def onExit(self, e):
        self.window.myFinder = None

    def drawPeople(self, fileNames):
        """Show in the scene the photos."""
        # TODO fix this
        # self.removeFromScene()
        posx = posy = 0
        for i in fileNames:
            pix = QtGui.QPixmap(i)
            sca = PixmapItem(pix.scaledToWidth(90), i)
            sca.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
            self.window.ui.scene.addItem(sca)
            if (self.window.ui.graphicsView.width() < (posx + 100)):
                posy += sca.pixmap().height() + 10
                posx = 0
            sca.setPos(posx, posy)
            posx += sca.pixmap().width() + 10


class State_LanmarkingSelection(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window
    
    def onEntry(self, e):
        self.showPreferences()
        self.window.ui.pushButton_3.setEnabled(True)

    def onExit(self, e):
        pass

    def showPreferences(self):
        """ Dialog for select the anatomic parts to evaluate."""
        #self.window.ui.pushButton_3.setEnabled(False)
        options = DialogOptions()
        if options.ui.listWidget.selectedItems():
            self.window.numberOfLandmarks = [int(x.text())
                                      for x in options.ui.listWidget.selectedItems()]
        else:
            self.window.numberOfLandmarks = [i for i in range(self.window.landn)]
        


class State_runLandmarking(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        self.window.count = 0

        self.window.ui.myButtonNext = MyButton("UI/Icons/next.png", "Next ..")
        self.window.ui.myButtonPrev = MyButton("UI/Icons/prev.png", "Prev ..")
        self.window.ui.myButtonEdit = MyButton("UI/Icons/learn.png", "Edit ..")
        self.window.ui.myButtonNext.clicked.connect(self.window.next)
        self.window.ui.myButtonEdit.clicked.connect(self.window.edit)
        self.window.ui.myButtonPrev.clicked.connect(self.window.prev)
        #TODO make an inner state machine
        self.window.ui.scene.buttonsForChecker(
            self.window.ui.myButtonNext, self.window.ui.myButtonEdit, self.window.ui.myButtonPrev)
        self.run()
        

    def onExit(self, e):
        pass

    def run(self):
        # TODO clean this
        self.window.removeFromScene()
        self.window.myFinder = Finder(self.window.photosNames)
        QtGui.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.window.myFinder.findLandmarks()
        QtGui.QApplication.restoreOverrideCursor()

        self.window.images = self.window.myFinder.drawLandmarks(self.window.numberOfLandmarks)
       

        self.window.drawLandmarks()

        #make small FA for this one
        self.window.ui.myButtonPrev.setVisible(True)
        self.window.ui.myButtonEdit.setVisible(True)
        self.window.ui.myButtonNext.setVisible(True)
        self.window.ui.myButtonPrev.setEnabled(False)
        self.window.ui.myButtonNext.setEnabled(True)

        self.ui.window.pushButton_4.setEnabled(True)


class State_saveLandmarking(QtCore.QState):

    def __init__(self, machine):
        QtCore.QState.__init__(self, machine)

    def onEntry(self, e):
        pass

    def onExit(self, e):
        pass


class State_clear(QtCore.QState):

    def __init__(self, machine):
        QtCore.QState.__init__(self, machine)

    def onEntry(self, e):
        pass

    def onExit(self, e):
        pass
