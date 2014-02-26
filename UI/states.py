#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import os
import logging
from PyQt4 import QtCore, QtGui
from popeye.UI.pixmapItem import PixmapItem
from popeye.UI.dialogOptions import DialogOptions
from ..finder import Finder
from popeye.utils.export import SaveFile


GETPHOTOSNAMES = lambda items: [i.path for i in filter(
    lambda x: isinstance(x, PixmapItem) and x.isVisible(), items)]



class NoImagesException(Exception):
    """Exception for no images loaded"""

    def __init__(self):
        Exception.__init__(self, "You must load some images")


class NolandmarksException(Exception):
    """Exception for no images selected"""

    def __init__(self):
        Exception.__init__(self, "You must select some landmarks")


class StateInit(QtCore.QState):
    """Initial State for setup the bar-buttons"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        """Put initial buttons off"""

        self.window.pushButton_2.setEnabled(False)
        self.window.pushButton_3.setEnabled(False)
        self.window.pushButton_4.setEnabled(False)

    def onExit(self, event):
        pass


class StateImageLoading(QtCore.QState):
    """In this state we present the image dialog loading and
    draw the small pictures."""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        """Pop-Up the Images Selection Dialog
        and draw the pictures in the scene."""

        dialog = QtGui.QFileDialog()
        try:
            outFileNames = dialog.getOpenFileNames(self.window, "Open Image",
                           self.window.settings.value("last_dir").toString(), "Image Files (*.png *.jpg *.bmp)")
            if not outFileNames:
                raise NoImagesException()
        except NoImagesException, exc:
            logging.error(exc.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window,
                                      "Warning",
                                      exc.message)
        else:
            self.window.settings.setValue("last_dir", os.path.split(outFileNames[0]))
            QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.draw_little_people(outFileNames)
            QtGui.QApplication.restoreOverrideCursor()
            self.window.ui.pushButton_2.setEnabled(True)

    def onExit(self, event):
        """Create the finder variable."""

        self.window.myfinder = None


    def draw_little_people(self, fileNames):
        """Show in the scene the photos."""

        # TODO fix this
        posx = posy = 0
        for i in fileNames:
            pix = QtGui.QPixmap(i)
            sca = PixmapItem(pix.scaledToWidth(90), i, self.window.ui.scene)
            sca.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
            if self.window.ui.graphicsView.width() < (posx + 100):
                posy += sca.pixmap().height() + 10
                posx = 0
                if posy >= self.window.ui.scene.height() - posy:
                    self.window.ui.scene.setSceneRect(0, 0, self.window.ui.scene.width(), 
                                         self.window.ui.scene.height() + sca.pixmap().height() + 10)
            sca.setPos(posx, posy)
            posx += sca.pixmap().width() + 10


class StateLanmarkingSelection(QtCore.QState):
    """In this state we select wich landmarks we want to
    see in the pictures"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        self.show_preferences()

    def onExit(self, event):
        pass

    def show_preferences(self):
        """ Dialog for select the anatomic parts to evaluate."""

        try:
            if not GETPHOTOSNAMES(self.window.ui.scene.items()):
                raise NoImagesException
            else:
                options = DialogOptions()
                if options.ui.listWidget.selectedItems():
                    self.window.numberOfLandmarks = [int(x.text())
                    for x in options.ui.listWidget.selectedItems()]

                    self.window.ui.pushButton_3.setEnabled(True)
                else:
                    raise NolandmarksException

        except (NoImagesException, NolandmarksException) as exc:
            logging.error(exc.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window, "Warning", exc.message)


class StateRunLandmarking(QtCore.QState):
    """Call the python-STASM bindings for the landmarking"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        pass

    def onExit(self, event):
        pass


class StateInitRun(QtCore.QState):

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        """Run the landmarking in the selected pictures."""

        try:
            self.window.count = 0
            photosnames = GETPHOTOSNAMES(self.window.ui.scene.items())
            if not photosnames:
                raise NoImagesException()
        except NoImagesException, e:
            logging.error(e.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window,
                                      "Warning",
                                      e.message)
        else:
            self.run(photosnames)
            self.window.ui.myButtonPrev.setVisible(True)
            self.window.ui.myButtonNext.setVisible(True)
            self.window.ui.myButtonEdit.setVisible(True)
            self.window.ui.pushButton_4.setEnabled(True)

    def onExit(self, event):
        pass

    def clear(self):
        #TODO this has to be in clean state
        #FIX THIS!
        items = self.window.ui.scene.items()
        images = filter(lambda x: x.isVisible() and not isinstance(
            x, QtGui.QGraphicsProxyWidget), items)
        map(lambda i: self.window.ui.scene.removeItem(i), images)
        self.window.ui.scene.setSceneRect(0, 0, self.window.ui.scene.width(), 300)

    def run(self, photosnames):
        if not self.window.myfinder:
            self.window.myfinder = Finder(photosnames)
            QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.window.myfinder.find_landmarks()
            QtGui.QApplication.restoreOverrideCursor()

        self.window.images = self.window.myfinder.draw_landmarks(
            self.window.numberOfLandmarks)
        self.clear()
        self.window.draw_landmarks_in_scene()


class StateFoward(QtCore.QState):
    """Move to the next picture."""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        if 0 <= self.window.count < len(self.window.images) - 1:
            self.window.count += 1
            self.window.draw_landmarks_in_scene()
            if not self.window.ui.myButtonPrev.isEnabled():
                self.window.ui.myButtonPrev.setEnabled(True)
        else:
            self.window.ui.myButtonNext.setEnabled(False)

    def onExit(self, event):
        pass


class StateBack(QtCore.QState):
    """Move to the previous picture."""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        if 0 < self.window.count < len(self.window.images):
            self.window.count -= 1
            self.window.draw_landmarks_in_scene()
            if not self.window.ui.myButtonNext.isEnabled():
                self.window.ui.myButtonNext.setEnabled(True)
        else:
            self.window.ui.myButtonPrev.setEnabled(False)

    def onExit(self, event):
        pass


class StateEdit(QtCore.QState):
    """Open the Dialog to change the position on landmarks."""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        pass

    def onExit(self, event):
        pass


class StateSaveLandmarking(QtCore.QState):
    """Show the save Dialog and call the export module."""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        dialog = QtGui.QFileDialog()
        savefilename = dialog.getSaveFileName(self.window, "Save File",
                                              os.getcwd(),
        
                                              "Files (*.txt *.tps *.xls *.cvs)")
        try:
            mysavefile = SaveFile(
                self.window.myfinder.filenames, savefilename,
                self.window.myfinder.landmarks, self.window.numberOfLandmarks)
            mysavefile.save()
        except IOError, exc:
            logging.error(exc.message, exc_info=True)
            QtGui.QMessageBox.warning(self.window,
                                      "Warning",
                                      "You have to choose a filename for the output")

    def onExit(self, event):
        pass


class StateClear(QtCore.QState):
    """Remove and/or set invisible the items in the
    scene."""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):

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
        self.window.ui.scene.setSceneRect(0, 0, self.window.ui.scene.width(), 300)

        self.finished.emit()

    def onExit(self, event):
        pass


class StateAbout(QtCore.QState):
    """Show the Credits Dialog"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        """Credits."""

        text = u"""<font color=black> PopEye is made in Python and C++
        using several libraries such as:
        numpy, scikit-image, STASM (with ctypes), scikit-learn.
        All the develop is made by people of GIBEH, CENPAT-CONICET.<br></font>
        """
        return QtGui.QMessageBox.about(self.window, u"About PopEye", text)

    def onExit(self, event):
        pass


class StateExit(QtCore.QState):
    """Exit state show the exit dialog"""

    def __init__(self, machine, window):
        QtCore.QState.__init__(self, machine)
        self.window = window

    def onEntry(self, event):
        """Exit dialog."""

        reply = QtGui.QMessageBox.question(
            self.window, 'Message', "Do you really want to go??",
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    def onExit(self, event):
        pass
