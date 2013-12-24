#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import sys
import logging
from PyQt4 import QtGui, QtCore
from UI.mainWindow import Main_Window


def main():

    logging.basicConfig(filename='Logs/popeye.log') #, level=logging.INFO)
    logging.info('Popeye Started')
    app = QtGui.QApplication(sys.argv)

    window = Main_Window()
    window.move(300, 100)
    window.show()

    sys.exit(app.exec_())
    logging.info('Popeye Finished')

if __name__ == "__main__":
    main()
