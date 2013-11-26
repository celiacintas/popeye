#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


class Table(QtGui.QTableView):

    def __init__(self, vHead, hHead, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)
        self.setModel(MyModel(vHead, hHead, len(vHead), len(hHead)))
        self.setAlternatingRowColors(True)
        #self.setFixedSize(230, 450)
        

class MyModel(QtGui.QStandardItemModel):

    def __init__(self, vHead, hHead, *args, **kwargs):
        QtGui.QStandardItemModel.__init__(self, *args, **kwargs)
        for j, i in zip(range(len(vHead)), vHead):
            self.setHeaderData(j, QtCore.Qt.Vertical, i)
        for j, i in zip(range(len(hHead)), hHead):
            self.setHeaderData(j, QtCore.Qt.Horizontal, i)

    def __getitem__(self, indice):
        #return self.index(indice[0], indice[1]).data().toPyObject()
        return self.index(indice[0], indice[1]).data().toReal()

    def __setitem__(self, indice, dato):
        indiceTabla = self.index(indice[0], indice[1])
        self.setData(indiceTabla, QtCore.QVariant(dato))
