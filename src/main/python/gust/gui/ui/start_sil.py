# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/workspaces/gust/src/main/python/gust/gui/ui/start_sil.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(589, 307)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout.setObjectName("formLayout")
        self.label_nameinput = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_nameinput.setFont(font)
        self.label_nameinput.setObjectName("label_nameinput")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label_nameinput
        )
        self.comboBox_type = QtWidgets.QComboBox(Dialog)
        self.comboBox_type.setMinimumSize(QtCore.QSize(130, 0))
        self.comboBox_type.setObjectName("comboBox_type")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.comboBox_type
        )
        self.label_select_home = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_select_home.setFont(font)
        self.label_select_home.setObjectName("label_select_home")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.label_select_home
        )
        self.comboBox_select_home = QtWidgets.QComboBox(Dialog)
        self.comboBox_select_home.setMinimumSize(QtCore.QSize(130, 0))
        self.comboBox_select_home.setObjectName("comboBox_select_home")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.comboBox_select_home
        )
        self.label_home_lat = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_home_lat.setFont(font)
        self.label_home_lat.setObjectName("label_home_lat")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.label_home_lat
        )
        self.lineEdit_home_lat = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_home_lat.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_home_lat.setObjectName("lineEdit_home_lat")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_home_lat
        )
        self.label_home_lon = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_home_lon.setFont(font)
        self.label_home_lon.setObjectName("label_home_lon")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.label_home_lon
        )
        self.lineEdit_home_lon = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_home_lon.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_home_lon.setObjectName("lineEdit_home_lon")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_home_lon
        )
        self.label_start_heading = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_start_heading.setFont(font)
        self.label_start_heading.setObjectName("label_start_heading")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.LabelRole, self.label_start_heading
        )
        self.lineEdit_start_heading = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_start_heading.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_start_heading.setObjectName("lineEdit_start_heading")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_start_heading
        )
        self.label_start_altitude = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_start_altitude.setFont(font)
        self.label_start_altitude.setObjectName("label_start_altitude")
        self.formLayout.setWidget(
            6, QtWidgets.QFormLayout.LabelRole, self.label_start_altitude
        )
        self.lineEdit_start_altitude = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_start_altitude.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_start_altitude.setObjectName("lineEdit_start_altitude")
        self.formLayout.setWidget(
            6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_start_altitude
        )
        self.label_sil_name = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_sil_name.setFont(font)
        self.label_sil_name.setObjectName("label_sil_name")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_sil_name
        )
        self.lineEdit_sil_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_sil_name.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_sil_name.setObjectName("lineEdit_sil_name")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_sil_name
        )
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_start = QtWidgets.QPushButton(Dialog)
        self.pushButton_start.setStyleSheet("background-color: rgb(138, 226, 52);")
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_nameinput.setText(_translate("Dialog", "Enter Vehicle's Type"))
        self.label_select_home.setText(_translate("Dialog", "Select Home"))
        self.label_home_lat.setText(_translate("Dialog", "Home Latitude"))
        self.label_home_lon.setText(_translate("Dialog", "Home Longitude"))
        self.label_start_heading.setText(_translate("Dialog", "Start Heading"))
        self.label_start_altitude.setText(_translate("Dialog", "Start Altitude (m)"))
        self.label_sil_name.setText(_translate("Dialog", "SIL Name"))
        self.pushButton_start.setText(_translate("Dialog", "START"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
