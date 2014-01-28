#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class Scene(QtGui.QGraphicsScene):

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

    def buttonsForChecker(self, myButtonNext, myButtonEdit, myButtonPrev):
        """ """

        proxyBotonEdit = QtGui.QGraphicsProxyWidget()
        proxyBotonNext = QtGui.QGraphicsProxyWidget()
        proxyBotonPrev = QtGui.QGraphicsProxyWidget()
        proxyBotonEdit.setWidget(myButtonEdit)
        proxyBotonNext.setWidget(myButtonNext)
        proxyBotonPrev.setWidget(myButtonPrev)
        proxyBotonNext.setPos(self.width() - 20, self.height())
        proxyBotonEdit.setPos(self.width() - 85, self.height())
        proxyBotonPrev.setPos(self.width() - 150, self.height())
        self.addItem(proxyBotonNext)
        self.addItem(proxyBotonEdit)
        self.addItem(proxyBotonPrev)

    def mousePressEvent(self, event):
        """ """
        item = self.itemAt(event.scenePos())
        self.sendEvent(item, event)
        print event.scenePos()

    def mouseReleaseEvent(self, event):
        """" """
        item = self.itemAt(event.scenePos())
        self.sendEvent(item, event)
