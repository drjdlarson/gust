# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/conn.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 259)
        MainWindow.setMaximumSize(QtCore.QSize(540, 260))
        MainWindow.setStyleSheet("background-color: rgb(211, 215, 207);\n"
"color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(340, 190))
        self.centralwidget.setMaximumSize(QtCore.QSize(540, 260))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout.setObjectName("formLayout")
        self.label_nameinput = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_nameinput.setFont(font)
        self.label_nameinput.setObjectName("label_nameinput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_nameinput)
        self.lineEdit_nameinput = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_nameinput.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.lineEdit_nameinput.setText("")
        self.lineEdit_nameinput.setObjectName("lineEdit_nameinput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_nameinput)
        self.label_port = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_port.setFont(font)
        self.label_port.setObjectName("label_port")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_port)
        self.comboBox_port = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_port.setObjectName("comboBox_port")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_port)
        self.label_baud = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_baud.setFont(font)
        self.label_baud.setObjectName("label_baud")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_baud)
        self.comboBox_baud = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_baud.setObjectName("comboBox_baud")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_baud)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setStyleSheet("background-color: rgb(138, 226, 52);")
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.horizontalLayout.addWidget(self.pushButton_connect)
        self.pushButton_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_nameinput.setText(_translate("MainWindow", "Enter Vehicle\'s Name"))
        self.label_port.setText(_translate("MainWindow", "PORT"))
        self.label_baud.setText(_translate("MainWindow", "BAUD"))
        self.pushButton_connect.setText(_translate("MainWindow", "CONNECT"))
        self.pushButton_cancel.setText(_translate("MainWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

