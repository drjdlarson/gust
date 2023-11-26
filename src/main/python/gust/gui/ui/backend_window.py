# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/workspaces/gust/src/main/python/gust/gui/ui/backend_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BackendWindow(object):
    def setupUi(self, BackendWindow):
        BackendWindow.setObjectName("BackendWindow")
        BackendWindow.resize(914, 745)
        self.centralwidget = QtWidgets.QWidget(BackendWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.listWidget_availPlugins = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_availPlugins.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.listWidget_availPlugins.setAlternatingRowColors(True)
        self.listWidget_availPlugins.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.listWidget_availPlugins.setObjectName("listWidget_availPlugins")
        self.gridLayout.addWidget(self.listWidget_availPlugins, 3, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setFlat(False)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.gridLayout_5.addWidget(self.pushButton_stop, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_5.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_5.addWidget(self.pushButton_start, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.gridLayout.addLayout(self.verticalLayout_3, 3, 4, 1, 1)
        self.label_port = QtWidgets.QLabel(self.centralwidget)
        self.label_port.setObjectName("label_port")
        self.gridLayout.addWidget(self.label_port, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lineEdit_IP = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.gridLayout.addWidget(self.lineEdit_IP, 0, 1, 1, 1)
        self.lineEdit_port = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.gridLayout.addWidget(self.lineEdit_port, 1, 1, 1, 1)
        self.label_IP = QtWidgets.QLabel(self.centralwidget)
        self.label_IP.setObjectName("label_IP")
        self.gridLayout.addWidget(self.label_IP, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_plugScan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plugScan.setObjectName("pushButton_plugScan")
        self.verticalLayout_2.addWidget(self.pushButton_plugScan)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_addPlugin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_addPlugin.setObjectName("pushButton_addPlugin")
        self.gridLayout_3.addWidget(self.pushButton_addPlugin, 0, 0, 1, 1)
        self.pushButton_removePlugin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_removePlugin.setObjectName("pushButton_removePlugin")
        self.gridLayout_3.addWidget(self.pushButton_removePlugin, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_2, 3, 2, 1, 1)
        self.selPluginsView = QtWidgets.QTableView(self.centralwidget)
        self.selPluginsView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.selPluginsView.setAlternatingRowColors(True)
        self.selPluginsView.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.selPluginsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.selPluginsView.setObjectName("selPluginsView")
        self.selPluginsView.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.selPluginsView, 3, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.textEdit_output = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(9)
        self.textEdit_output.setFont(font)
        self.textEdit_output.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit_output.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse
        )
        self.textEdit_output.setObjectName("textEdit_output")
        self.verticalLayout.addWidget(self.textEdit_output)
        BackendWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BackendWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 22))
        self.menubar.setObjectName("menubar")
        BackendWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BackendWindow)
        self.statusbar.setObjectName("statusbar")
        BackendWindow.setStatusBar(self.statusbar)

        self.retranslateUi(BackendWindow)
        QtCore.QMetaObject.connectSlotsByName(BackendWindow)

    def retranslateUi(self, BackendWindow):
        _translate = QtCore.QCoreApplication.translate
        BackendWindow.setWindowTitle(_translate("BackendWindow", "Backend Console"))
        self.label_2.setText(_translate("BackendWindow", "Selected Plugins:"))
        self.pushButton_stop.setText(_translate("BackendWindow", "Stop"))
        self.pushButton_start.setText(_translate("BackendWindow", "Start"))
        self.label_port.setText(_translate("BackendWindow", "Port:"))
        self.label.setText(_translate("BackendWindow", "Available Plugins:"))
        self.lineEdit_IP.setText(_translate("BackendWindow", "127.0.0.1"))
        self.lineEdit_port.setText(_translate("BackendWindow", "8000"))
        self.label_IP.setText(_translate("BackendWindow", "IP Address:"))
        self.pushButton_plugScan.setText(_translate("BackendWindow", "Rescan Plugins"))
        self.pushButton_addPlugin.setText(_translate("BackendWindow", "Add"))
        self.pushButton_removePlugin.setText(_translate("BackendWindow", "Remove"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    BackendWindow = QtWidgets.QMainWindow()
    ui = Ui_BackendWindow()
    ui.setupUi(BackendWindow)
    BackendWindow.show()
    sys.exit(app.exec_())
