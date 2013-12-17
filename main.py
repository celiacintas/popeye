#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import sys
from PyQt4 import QtGui, QtCore
from UI.mainWindow import Main_Window


def main():

    app = QtGui.QApplication(sys.argv)
  
    window = Main_Window()
    window.move(300, 100)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
