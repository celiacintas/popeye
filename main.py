#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

import sys
import os
import logging
from PyQt4 import QtGui
from popeye.UI.mainwindow import MainWindow

FILELOGS = os.path.join(os.path.dirname(__file__), 'logs/popeye.log')


def main():
    """Activate the logging and run PopEye!!"""
    logging.basicConfig(filename=FILELOGS)  # , level=logging.INFO)
    logging.info('Popeye Started')
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.move(300, 100)
    window.show()

    sys.exit(app.exec_())
    logging.info('Popeye Finished')

if __name__ == "__main__":
    main()
