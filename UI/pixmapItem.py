#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class PixmapItem(QtGui.QGraphicsPixmapItem):

    def __init__(self, pixmap, path, parent=None):
        super(PixmapItem, self).__init__(parent)
        self.setPixmap(pixmap)
        self.path = path

    """
    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        self.setOpacity(1.0)
    """

    def contextMenuEvent(self, contextEvent):
        """Option to delete the photo"""
        menu = QtGui.QMenu()
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(contextEvent.screenPos())
        if (action == deleteAction):
            self.setVisible(False)
