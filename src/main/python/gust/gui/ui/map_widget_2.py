#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:04:33 2022

@author: lagerprocessor
"""

from qgis.gui import *
from PyQt5.QtGui import QAction, QMainWindow


class Map_Widget(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)
        self.setWindowTitle('Map Canvas from QGIS')



if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = Map_Widget()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
