# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/server_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(914, 745)
        self.centralwidget = QtWidgets.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_IP = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.gridLayout.addWidget(self.lineEdit_IP, 0, 1, 1, 1)
        self.lineEdit_port = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.gridLayout.addWidget(self.lineEdit_port, 1, 1, 1, 1)
        self.listWidget_availPlugins = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_availPlugins.setObjectName("listWidget_availPlugins")
        self.gridLayout.addWidget(self.listWidget_availPlugins, 3, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_plugScan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plugScan.setObjectName("pushButton_plugScan")
        self.verticalLayout_3.addWidget(self.pushButton_plugScan)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_removePlugin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_removePlugin.setObjectName("pushButton_removePlugin")
        self.gridLayout_5.addWidget(self.pushButton_removePlugin, 1, 1, 1, 1)
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setFlat(False)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.gridLayout_5.addWidget(self.pushButton_stop, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_5.addWidget(self.pushButton_start, 3, 0, 1, 1)
        self.pushButton_addPlugin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_addPlugin.setObjectName("pushButton_addPlugin")
        self.gridLayout_5.addWidget(self.pushButton_addPlugin, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.gridLayout.addLayout(self.verticalLayout_3, 3, 4, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_IP = QtWidgets.QLabel(self.centralwidget)
        self.label_IP.setObjectName("label_IP")
        self.gridLayout.addWidget(self.label_IP, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.listWidget_selPlugins = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_selPlugins.setObjectName("listWidget_selPlugins")
        self.gridLayout.addWidget(self.listWidget_selPlugins, 3, 3, 1, 1)
        self.label_port = QtWidgets.QLabel(self.centralwidget)
        self.label_port.setObjectName("label_port")
        self.gridLayout.addWidget(self.label_port, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.textEdit_output = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(9)
        self.textEdit_output.setFont(font)
        self.textEdit_output.setObjectName("textEdit_output")
        self.verticalLayout.addWidget(self.textEdit_output)
        ServerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ServerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 20))
        self.menubar.setObjectName("menubar")
        ServerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ServerWindow)
        self.statusbar.setObjectName("statusbar")
        ServerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ServerWindow)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerWindow.setWindowTitle(_translate("ServerWindow", "Backend Console"))
        self.lineEdit_IP.setText(_translate("ServerWindow", "127.0.0.1"))
        self.lineEdit_port.setText(_translate("ServerWindow", "8000"))
        self.pushButton_plugScan.setText(_translate("ServerWindow", "Rescan Plugins"))
        self.pushButton_removePlugin.setText(_translate("ServerWindow", "Remove"))
        self.pushButton_stop.setText(_translate("ServerWindow", "Stop"))
        self.pushButton_start.setText(_translate("ServerWindow", "Start"))
        self.pushButton_addPlugin.setText(_translate("ServerWindow", "Add"))
        self.label.setText(_translate("ServerWindow", "Available Plugins:"))
        self.label_IP.setText(_translate("ServerWindow", "IP Address:"))
        self.label_2.setText(_translate("ServerWindow", "Selected Plugins:"))
        self.label_port.setText(_translate("ServerWindow", "Port:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ServerWindow = QtWidgets.QMainWindow()
    ui = Ui_ServerWindow()
    ui.setupUi(ServerWindow)
    ServerWindow.show()
    sys.exit(app.exec_())
