#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:19:09 2022

@author: lagerprocessor
"""

import sys
import io
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

class HudWidget(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)
        self.setWindowTitle('Heads up Display GUST')

        layout = QVBoxLayout()
        self.setLayout(layout)

        button1=QPushButton("THIS IS THE HORIZON DISPLAY")
        layout.addWidget(button1,1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = HudWidget()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
