#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import sys
from PyQt4 import QtGui, QtCore
from UI.mainWindow import Main_Window

def main():

    app = QtGui.QApplication(sys.argv)
    splash_pix = QtGui.QPixmap('Icons/test.png')
    splash_pix = splash_pix.scaledToWidth(300)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()

    window = Main_Window()
    window.move(300, 100)
    window.show()


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
