# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/launcher.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Launcher(object):
    def setupUi(self, Launcher):
        Launcher.setObjectName("Launcher")
        Launcher.resize(390, 180)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Launcher.sizePolicy().hasHeightForWidth())
        Launcher.setSizePolicy(sizePolicy)
        Launcher.setMinimumSize(QtCore.QSize(390, 180))
        Launcher.setMaximumSize(QtCore.QSize(390, 180))
        Launcher.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(Launcher)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(300, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_server = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_server.sizePolicy().hasHeightForWidth())
        self.pushButton_server.setSizePolicy(sizePolicy)
        self.pushButton_server.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton_server.setObjectName("pushButton_server")
        self.horizontalLayout.addWidget(self.pushButton_server)
        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_client = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_client.sizePolicy().hasHeightForWidth())
        self.pushButton_client.setSizePolicy(sizePolicy)
        self.pushButton_client.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton_client.setObjectName("pushButton_client")
        self.horizontalLayout.addWidget(self.pushButton_client)
        spacerItem2 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_log = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_log.setObjectName("pushButton_log")
        self.horizontalLayout_2.addWidget(self.pushButton_log)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        Launcher.setCentralWidget(self.centralwidget)

        self.retranslateUi(Launcher)
        QtCore.QMetaObject.connectSlotsByName(Launcher)

    def retranslateUi(self, Launcher):
        _translate = QtCore.QCoreApplication.translate
        Launcher.setWindowTitle(_translate("Launcher", "gust launcher"))
        self.pushButton_server.setText(_translate("Launcher", "Server"))
        self.pushButton_client.setText(_translate("Launcher", "Client"))
        self.pushButton_log.setText(_translate("Launcher", "Log"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Launcher = QtWidgets.QMainWindow()
    ui = Ui_Launcher()
    ui.setupUi(Launcher)
    Launcher.show()
    sys.exit(app.exec_())

