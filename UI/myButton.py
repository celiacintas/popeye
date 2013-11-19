#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class MyButton(QtGui.QPushButton):
    
     def __init__(self, iconPath, tooltip, parent=None):
        super(MyButton, self).__init__(parent)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.On)
        
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(54, 54))
        self.setFlat(True)
        self.setCheckable(False)
        self.setStyleSheet("background-image:url(t.jpg);\n border-style: none;\n")
        self.setToolTip(QtGui.QApplication.translate("MainWindow", tooltip, None, QtGui.QApplication.UnicodeUTF8))
     