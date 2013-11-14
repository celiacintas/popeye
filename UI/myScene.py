#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#! /usr/bin/python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class okButton(QtGui.QPushButton):

    def __init__(self, parent=None):
        super(okButton, self).__init__()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("UI/Icons/apply.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setIcon(icon1)
        self.setIconSize(QtCore.QSize(64, 64))
        self.setCheckable(False)
        self.setFlat(True)

    def mousePressEvent(self, event):
        """ """
        #esta funcion tiene que limpiar de la scene los items
        # que estan invisibles

#TODO agregar botones de listo aca


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
        proxyBotonNext.setPos(self.width() - 45, self.height())
        proxyBotonEdit.setPos(self.width() - 110, self.height())
        proxyBotonPrev.setPos(self.width() - 175, self.height())
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

######################################################
