#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from PyQt4 import QtGui


class MyGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self)

    def resizeEvent(self, event):
            items = self.items()
            self.centerOn(1.0, 1.0)
            posx = posy = 0
            visibleItems = filter(lambda i: i.isVisible(), items)
            for i in visibleItems:
                if (self.width() < (posx + 100)):
                    posy += i.pixmap().height() + 10
                    posx = 0
                i.setPos(posx, posy)
                posx += i.pixmap().width() + 10


