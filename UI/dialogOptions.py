#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, QtCore
from opciones_UI import Ui_Dialog
from landmark import Landmark
import numpy as np
import skimage.io as io
from popeye.utils.qimage2ndarray import toqimage

STATIC_LANDMARKS = np.array([[751., 1199.], [767., 1368.], [801., 1518.],
                   [  855.,  1671.], [  962.,  1825.], [ 1107.,  1944.],
                   [ 1245.,  1973.], [ 1374.,  1951.], [ 1522.,  1848.],
                   [ 1648.,  1695.], [ 1700.,  1529.], [ 1727.,  1360.], 
                   [ 1736.,  1171.], [ 1456.,   740.], [ 1243.,   708.],
                   [ 1026.,   759.], [ 1030.,  1047.], [  917.,  1051.],
                   [  829.,  1133.], [  925.,  1111.], [ 1028.,  1107.],
                   [ 1137.,  1106.], [ 1319.,  1092.], [ 1424.,  1028.],
                   [ 1540., 1024.], [ 1635.,  1099.], [ 1534.,  1083.],
                   [ 1430., 1085.], [ 1442.,  1112.], [ 1010.,  1132.],
                   [ 1098., 1202.], [ 1054.,  1175.], [ 1008.,  1162.],
                   [  968.,  1174.], [  928.,  1206.], [  970.,  1226.],
                   [ 1011.,  1236.], [ 1055.,  1226.], [ 1008.,  1194.], 
                   [ 1438.,  1174.], [ 1357.,  1192.], [ 1400.,  1157.],
                   [ 1443.,  1143.], [ 1485.,  1154.], [ 1527.,  1180.],
                   [ 1486.,  1206.], [ 1445.,  1217.], [ 1401.,  1209.],
                   [ 1309.,  1366.], [ 1238.,  1368.], [ 1167.,  1369.],
                   [ 1166.,  1503.], [ 1239.,  1467.], [ 1314.,  1497.],
                   [ 1375.,  1452.], [ 1345.,  1507.], [ 1242.,  1545.],
                   [ 1138.,  1514.], [ 1107.,  1460.], [ 1061.,  1666.],
                   [ 1135.,  1643.], [ 1201.,  1631.], [ 1245.,  1637.],
                   [ 1288.,  1629.], [ 1357.,  1636.], [ 1433.,  1655.],
                   [ 1328.,  1661.], [ 1244.,  1667.], [ 1162.,  1667.],
                   [ 1160.,  1685.], [ 1244.,  1696.], [ 1328.,  1681.],
                   [ 1382.,  1708.], [ 1319.,  1738.], [ 1245.,  1749.],
                   [ 1172.,  1741.], [ 1111.,  1714.]])

class DialogOptions(QtGui.QDialog):

    def __init__(self, number_of_landmarks=77, parent=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.initUI(number_of_landmarks)

    def initUI(self, number_of_landmarks):
        self.ui.graphicsView.scale(0.21, 0.21)
        self.ui.scene = QtGui.QGraphicsScene()
        self.ui.scene.setSceneRect(QtCore.QRectF())
        self.ui.graphicsView.setScene(self.ui.scene)
        self.ui.graphicsView.setInteractive(True)
        #QtGui.QGraphicsPixmapItem(pixmap, scene=self.ui.scene)

        self.load_image(os.path.join(os.path.dirname(__file__), 
                        "Images/landmarking_1.jpg"))
        self.load_landmarks(range(number_of_landmarks))
        self.setWindowTitle('Landmarking Selection')
        self.exec_()

    def load_image(self, image_path):
        """Load Image in graphics view of dialog"""
        qitmp = toqimage(io.imread(image_path))
        pix = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(QtGui.QPixmap.fromImage(qitmp)), scene=self.ui.scene)

    def load_landmarks(self, number_landmarks):
        """Set pixmap items in landmarks position and set"""
        for n in number_landmarks:
            Landmark(n, STATIC_LANDMARKS[n][0], STATIC_LANDMARKS[n][1], 30, 30, scene=self.ui.scene, flag=QtGui.QGraphicsItem.ItemIsSelectable, text=True)

    def get_number_landmarks(self):
        """Return the number of landmarks in ascending order selected by ctrl + click to be used."""
        landmarks = filter(lambda x: isinstance(x, Landmark) and x.isSelected(), self.ui.scene.items())
        clear_landmarks = [l.nro_landmark for l in landmarks]
        clear_landmarks.reverse()
        return clear_landmarks