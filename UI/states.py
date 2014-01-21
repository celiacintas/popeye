#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import os
import sys
import logging
from PyQt4 import QtCore, QtGui
from UI.pixmapItem import PixmapItem
from UI.dialogOptions import DialogOptions
from UI.myButton import MyButton
from finder import Finder
from Utils.export import SaveFile


getPhotosNames = lambda items: [i.path for i in filter(
    lambda x: isinstance(x, PixmapItem) and x.isVisible(), items)]


class NoImagesException(Exception):

    def __init__(self):
        Exception.__init__(self, "You must load some images")


class NolandmarksException(Exception):

    def __init__(self):
        Exception.__init__(self, "You must select some landmarks")


class State_Init(QtCore.QState):

    """Initial State for setup the bar-buttons"""

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

    """In this state we present the image dialog loading and
    draw the small pictures"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        dialog = QtGui.QFileDialog()
        try:
            outFileNames = dialog.getOpenFileNames(self.window, "Open Image",
                                                   os.getcwd(),
                                                   "Image Files (*.png *.jpg *.bmp)")
            if not outFileNames:
                raise NoImagesException()
        except NoImagesException, e:
            logging.error(e.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window,
                                      "Warning",
                                      e.message)
        else:
            self.drawPeople(outFileNames)
            self.window.ui.pushButton_2.setEnabled(True)

    def onExit(self, e):
        self.window.myFinder = None

    def drawPeople(self, fileNames):
        """Show in the scene the photos."""
        # TODO fix this
        posx = posy = 0
        for i in fileNames:
            pix = QtGui.QPixmap(i)
            sca = PixmapItem(pix.scaledToWidth(90), i, self.window.ui.scene)
            sca.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
            if (self.window.ui.graphicsView.width() < (posx + 100)):
                posy += sca.pixmap().height() + 10
                posx = 0
            sca.setPos(posx, posy)
            posx += sca.pixmap().width() + 10


class State_LanmarkingSelection(QtCore.QState):

    """In this state we select wich landmarks we want to 
    see in the pictures"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        self.showPreferences()

    def onExit(self, e):
        pass

    def showPreferences(self):
        """ Dialog for select the anatomic parts to evaluate."""
        try:
            if not getPhotosNames(self.window.ui.scene.items()):
                raise NoImagesException
            else:
                options = DialogOptions()
                if options.ui.listWidget.selectedItems():
                    self.window.numberOfLandmarks = [int(x.text())
                                                     for x in options.ui.listWidget.selectedItems()]
                    self.window.ui.pushButton_3.setEnabled(True)
                else:
                    raise NolandmarksException

        except (NoImagesException, NolandmarksException) as e:
            logging.error(e.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window, "Warning", e.message)


class State_runLandmarking(QtCore.QState):

    """Call the python-STASM bindings for the landmarking"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        pass

    def onExit(self, e):
        pass


class State_init_run(QtCore.QState):

    def __init__(self, machine, window, parent=None):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        try:
            self.window.count = 0
            photosNames = getPhotosNames(self.window.ui.scene.items())
            if photosNames == []:
                raise NoImagesException()
        except NoImagesException, e:
            logging.error(e.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window,
                                      "Warning",
                                      e.message)
        else:
            self.run(photosNames)
            self.window.ui.myButtonPrev.setVisible(True)
            self.window.ui.myButtonNext.setVisible(True)
            self.window.ui.myButtonEdit.setVisible(True)
            self.window.ui.pushButton_4.setEnabled(True)

    def onExit(self, e):
        pass

    def run(self, photosNames):
        # TODO clean this
        if not self.window.myFinder:
            self.window.myFinder = Finder(photosNames)
            QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.window.myFinder.findLandmarks()
            QtGui.QApplication.restoreOverrideCursor()

        self.window.images = self.window.myFinder.drawLandmarks(
            self.window.numberOfLandmarks)
        self.window.drawLandmarks()


class State_foward(QtCore.QState):

    def __init__(self, machine, window, parent=None):
        QtCore.QState.__init__(self, machine)
        self.window = window


    def onEntry(self, e):
        if 0 <= self.window.count < len(self.window.images) - 1:
            self.window.count += 1
            self.window.drawLandmarks()
            if not self.window.ui.myButtonPrev.isEnabled():
                self.window.ui.myButtonPrev.setEnabled(True)
        else:
            self.window.ui.myButtonNext.setEnabled(False)

    def onExit(self, e):
        pass


class State_back(QtCore.QState):

    def __init__(self, machine, window, parent=None):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        if 0 < self.window.count < len(self.window.images):
            self.window.count -= 1
            self.window.drawLandmarks()
            if not self.window.ui.myButtonNext.isEnabled():
                self.window.ui.myButtonNext.setEnabled(True)
        else:
            self.window.ui.myButtonPrev.setEnabled(False)

    def onExit(self, e):
        pass


class State_edit(QtCore.QState):

    def __init__(self, machine, window, parent=None):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        pass

    def onExit(self, e):
        pass


class State_saveLandmarking(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        dialog = QtGui.QFileDialog()
        saveFileName = dialog.getSaveFileName(self.window, "Save File",
                                              os.getcwd(),
                                              "Files (*.txt *.tps *.xls *.cvs)")
        mySaveFile = SaveFile(
            saveFileName, self.window.myFinder.landmarks, self.window.numberOfLandmarks)
        mySaveFile.save()

    def onExit(self, e):
        pass


class State_clear(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        items = self.window.ui.scene.items()
        images = filter(lambda x: x.isVisible() and not isinstance(
            x, QtGui.QGraphicsProxyWidget), items)
        buttons = filter(lambda x: x.isVisible() and isinstance(
            x, QtGui.QGraphicsProxyWidget), items)
        # remove all the image and tables but hide the buttons
        # nasty fix
        map(lambda i: self.window.ui.scene.removeItem(i), images)
        map(lambda b: b.setVisible(False), buttons)
        map(lambda b: b.setEnabled(True), buttons)

        self.finished.emit()

    def onExit(self, e):
        pass


class State_about(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        """Credits."""
        text = u"""<font color=black> PopEye is made in Python and C++ using several libraries such as:
        numpy, scikit-image, STASM (with ctypes), scikit-learn.
        All the develop is made by people of GIBEH, CENPAT-CONICET.<br></font>
        """
        return QtGui.QMessageBox.about(self.window, u"About PopEye", text)

    def onExit(self, e):
        pass


class State_exit(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, e):
        """Exit dialog."""
        reply = QtGui.QMessageBox.question(
            self.window, 'Message', "Do you really want to go??", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    def onExit(self, e):
        pass
