#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import os
import sys
from finder import Finder
from PyQt4 import QtCore, QtGui
from UI.popEye_UI import Ui_MainWindow
from UI.pixmapItem import PixmapItem
from UI.dialogOptions import DialogOptions
from UI.myButton import MyButton
from UI.myScene import Scene
from UI.table import Table
from Utils.qimage2ndarray import toQImage
from Utils.export import SaveFile



class Main_Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.scene = Scene()
        self.ui.scene.setSceneRect(0, 0, 700, 300)
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        self.ui.actionInteractive_Mode.triggered.connect(self.showFileDialog)
        self.ui.actionLandmark_Configuration.triggered.connect(self.showPreferences)
        self.ui.actionAbout.triggered.connect(self.showAbout)
        self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.ui.pushButton.clicked.connect(self.showFileDialog)
        self.ui.pushButton_2.clicked.connect(self.showPreferences)
        self.ui.pushButton_3.clicked.connect(self.run)
        self.ui.pushButton_4.clicked.connect(self.save)
        self.ui.pushButton_6.clicked.connect(self.showAbout)
        self.ui.pushButton_5.clicked.connect(self.showQuit)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.myButtonNext = MyButton("UI/Icons/next.png", "Next ..")
        self.ui.myButtonPrev = MyButton("UI/Icons/prev.png", "Prev ..")
        self.ui.myButtonEdit = MyButton("UI/Icons/learn.png", "Edit ..")
        self.ui.myButtonNext.clicked.connect(self.next)
        self.ui.myButtonEdit.clicked.connect(self.edit)
        self.ui.myButtonPrev.clicked.connect(self.prev)
        self.ui.scene.buttonsForChecker(self.ui.myButtonNext, self.ui.myButtonEdit, self.ui.myButtonPrev)
        self.ui.myButtonPrev.setVisible(False) 
        self.ui.myButtonEdit.setVisible(False)
        self.ui.myButtonNext.setVisible(False)
        self.ui.graphicsView.show()
        self.photosNames = list()
        

    def bienvenida(self):
        """benbenute"""
        text = u"""<font color=black> Welcome to PopEye!If this is your
        first time see this <a href="www.youtube.com/watch?v=Al9EgCJ6LHY">
        video</a>.</font>"""
        return QtGui.QMessageBox.about(self, "Welcome to PopEye", text)

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
        

    def showFileDialog(self):
        """ Face loading dialog."""
        dialog = QtGui.QFileDialog()
        outFileNames = dialog.getOpenFileNames(self, "Open Image",
                                      os.getcwd(),
                                      "Image Files (*.png *.jpg *.bmp)")
        self.drawPeople(outFileNames)
        self.photosNames = outFileNames
        self.ui.pushButton_2.setEnabled(True)

    def showPreferences(self):
        """ Dialog for select the anatomic parts to evaluate."""
        options = DialogOptions()
        if options.ui.listWidget.selectedItems():
            self.numberOfLandmarks = [int(x.text()) for x in options.ui.listWidget.selectedItems()]
        else:
            self.numberOfLandmarks = [i for i in range(77)]
        self.ui.pushButton_3.setEnabled(True)
        

    def run(self):
        #TODO clean this
        items = self.ui.scene.items()
        for i in items:
            if isinstance(i, PixmapItem) and not i.isVisible():
                self.photosNames.remove(i.path)
            elif isinstance(i, PixmapItem):
                self.ui.scene.removeItem(i)
        
        self.myFinder = Finder(self.photosNames)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.myFinder.findLandmarks()
        QtGui.QApplication.restoreOverrideCursor()
        self.images = self.myFinder.drawLandmarks(self.numberOfLandmarks)
        self.count = 0
        self.drawLandmarks()

        self.ui.myButtonPrev.setVisible(True) 
        self.ui.myButtonEdit.setVisible(True)
        self.ui.myButtonNext.setVisible(True)
        self.ui.myButtonPrev.setEnabled(False)
            
        self.ui.pushButton_4.setEnabled(True)

    def prev(self):
        if  0 < self.count <= len(self.images):
            self.count = self.count - 1
            self.drawLandmarks()
        else:
            self.ui.myButtonPrev.setEnabled(False)

        if not self.ui.myButtonNext.isEnabled():
            self.ui.myButtonNext.setEnabled(True)

    def next(self):
        if len(self.images)-1 > self.count:
            self.count = self.count + 1
            self.drawLandmarks()
        else:
            self.ui.myButtonNext.setEnabled(False)
        if not self.ui.myButtonPrev.isEnabled():
            self.ui.myButtonPrev.setEnabled(True)
        
    def save(self):
        dialog = QtGui.QFileDialog()
        saveFileName = dialog.getSaveFileName(self, "Save File",
                                      os.getcwd(),
                                      "Files (*.txt *.tps *.xls *.cvs)")
        mySaveFile = SaveFile(saveFileName, self.myFinder.landmarks)
        mySaveFile.save()

    def drawLandmarks(self):
            self.myTable = Table(self.numberOfLandmarks, ['x', 'y'])
            myLandmarks = self.myFinder.landmarks[self.count]
            myLandmarks2Table = [myLandmarks[i] for i in self.numberOfLandmarks]
            self.loadModel(myLandmarks2Table)
            proxyTabla = QtGui.QGraphicsProxyWidget()
            proxyTabla.setWidget(self.myTable)
            proxyTabla.setPos(320, 0)
            
            qitmp = toQImage(self.images[self.count])
            pix = QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp))
            sca = PixmapItem(pix.scaledToWidth(300), None)
            
            self.ui.scene.addItem(sca)
            self.ui.scene.addItem(proxyTabla)

    def loadModel(self, landmarks):
        myModel = self.myTable.model()
        for i in range(len(landmarks)):
            for j in range(len(landmarks[0])):
                myModel[i, j] = float(landmarks[i][j])
                
    def edit(self):
        pass

    def saveLandmarks(self):
        if not self.ui.myButtonPrev.isEnabled():
            self.ui.myButtonPrev.setEnabled(True)


    def drawPeople(self, fileNames):
        """Show in the scene the photos."""
        #TODO fix this
        posx = posy = 0
        for i in fileNames:
            pix = QtGui.QPixmap(i)
            sca = PixmapItem(pix.scaledToWidth(90), i)
            sca.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
            self.ui.scene.addItem(sca)
            if (self.ui.graphicsView.width() < (posx + 100)):
                posy += sca.pixmap().height() + 10
                posx = 0
            sca.setPos(posx, posy)
            posx += sca.pixmap().width() + 10