#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from PyQt4 import QtGui
from opciones_UI import Ui_Dialog


class DialogOptions(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI()
           
    def initUI(self):      
        pixmap = QtGui.QPixmap("UI/Images/landmarking.jpg")
        for i in range(72):
            item = QtGui.QListWidgetItem("%i" % i)
            self.ui.listWidget.addItem(item)       
        
        self.ui.label.setPixmap(pixmap)
   
        self.setWindowTitle('Landmarking Selection')
        self.exec_()
        