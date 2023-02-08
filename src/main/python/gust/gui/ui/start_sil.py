# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/start_sil.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 260)
        MainWindow.setMinimumSize(QtCore.QSize(340, 190))
        MainWindow.setMaximumSize(QtCore.QSize(540, 260))
        MainWindow.setStyleSheet("background-color: rgb(211, 215, 207);\n"
"color: rgb(0, 0, 0);")
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout.setObjectName("formLayout")
        self.label_nameinput = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_nameinput.setFont(font)
        self.label_nameinput.setObjectName("label_nameinput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_nameinput)
        self.comboBox_type = QtWidgets.QComboBox(MainWindow)
        self.comboBox_type.setMinimumSize(QtCore.QSize(130, 0))
        self.comboBox_type.setObjectName("comboBox_type")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_type)
        self.lineEdit_home_lon = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_home_lon.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_home_lon.setObjectName("lineEdit_home_lon")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_home_lon)
        self.lineEdit_home_lat = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_home_lat.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_home_lat.setObjectName("lineEdit_home_lat")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_home_lat)
        self.label_home_lat = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_home_lat.setFont(font)
        self.label_home_lat.setObjectName("label_home_lat")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_home_lat)
        self.label_home_lon = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_home_lon.setFont(font)
        self.label_home_lon.setObjectName("label_home_lon")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_home_lon)
        self.label_framerate = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_framerate.setFont(font)
        self.label_framerate.setObjectName("label_framerate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_framerate)
        self.label_instance = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_instance.setFont(font)
        self.label_instance.setObjectName("label_instance")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_instance)
        self.lineEdit_framerate = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_framerate.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_framerate.setObjectName("lineEdit_framerate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_framerate)
        self.lineEdit_instance = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_instance.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_instance.setObjectName("lineEdit_instance")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_instance)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_start = QtWidgets.QPushButton(MainWindow)
        self.pushButton_start.setStyleSheet("background-color: rgb(138, 226, 52);")
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_cancel = QtWidgets.QPushButton(MainWindow)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_nameinput.setText(_translate("MainWindow", "Enter Vehicle\'s Type"))
        self.label_home_lat.setText(_translate("MainWindow", "Home Latitude"))
        self.label_home_lon.setText(_translate("MainWindow", "Home Longitude"))
        self.label_framerate.setText(_translate("MainWindow", "SIL Framerate"))
        self.label_instance.setText(_translate("MainWindow", "Instance (N)"))
        self.pushButton_start.setText(_translate("MainWindow", "START"))
        self.pushButton_cancel.setText(_translate("MainWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
