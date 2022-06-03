# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/hud_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_hud(object):
    def setupUi(self, Form_hud):
        Form_hud.setObjectName("Form_hud")
        Form_hud.resize(470, 441)
        Form_hud.setMinimumSize(QtCore.QSize(308, 308))
        Form_hud.setMouseTracking(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form_hud)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_top = QtWidgets.QFrame(Form_hud)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMinimumSize(QtCore.QSize(308, 25))
        self.frame_top.setMaximumSize(QtCore.QSize(180, 16777215))
        self.frame_top.setSizeIncrement(QtCore.QSize(0, 0))
        self.frame_top.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_top.setAutoFillBackground(False)
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_3.addWidget(self.frame_top)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_left = QtWidgets.QFrame(Form_hud)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_left.sizePolicy().hasHeightForWidth())
        self.frame_left.setSizePolicy(sizePolicy)
        self.frame_left.setMinimumSize(QtCore.QSize(30, 150))
        self.frame_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.horizontalLayout_2.addWidget(self.frame_left)
        self.frame_center = QtWidgets.QFrame(Form_hud)
        self.frame_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center.setObjectName("frame_center")
        self.horizontalLayout_2.addWidget(self.frame_center)
        self.frame_right = QtWidgets.QFrame(Form_hud)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_right.sizePolicy().hasHeightForWidth())
        self.frame_right.setSizePolicy(sizePolicy)
        self.frame_right.setMinimumSize(QtCore.QSize(30, 150))
        self.frame_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_right.setObjectName("frame_right")
        self.horizontalLayout_2.addWidget(self.frame_right)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_arm = QtWidgets.QLabel(Form_hud)
        font = QtGui.QFont()
        font.setFamily("Padauk Book [PYRS]")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_arm.setFont(font)
        self.label_arm.setStyleSheet("color:rgb(255, 0, 0);")
        self.label_arm.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_arm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_arm.setObjectName("label_arm")
        self.horizontalLayout.addWidget(self.label_arm)
        self.label_gnssfix = QtWidgets.QLabel(Form_hud)
        font = QtGui.QFont()
        font.setFamily("Padauk Book [PYRS]")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_gnssfix.setFont(font)
        self.label_gnssfix.setStyleSheet("color:rgb(255, 0, 0);")
        self.label_gnssfix.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_gnssfix.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gnssfix.setObjectName("label_gnssfix")
        self.horizontalLayout.addWidget(self.label_gnssfix)
        self.label_mode = QtWidgets.QLabel(Form_hud)
        font = QtGui.QFont()
        font.setFamily("Padauk Book [PYRS]")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_mode.setFont(font)
        self.label_mode.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_mode.setStyleSheet("color:rgb(255, 0, 0);")
        self.label_mode.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mode.setObjectName("label_mode")
        self.horizontalLayout.addWidget(self.label_mode)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Form_hud)
        QtCore.QMetaObject.connectSlotsByName(Form_hud)

    def retranslateUi(self, Form_hud):
        _translate = QtCore.QCoreApplication.translate
        Form_hud.setWindowTitle(_translate("Form_hud", "Form"))
        self.label_arm.setText(_translate("Form_hud", "ARMED"))
        self.label_gnssfix.setText(_translate("Form_hud", "3D FIX"))
        self.label_mode.setText(_translate("Form_hud", "AUTO"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_hud = QtWidgets.QWidget()
    ui = Ui_Form_hud()
    ui.setupUi(Form_hud)
    Form_hud.show()
    sys.exit(app.exec_())
