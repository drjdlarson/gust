# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/gustClient.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_main(object):
    def setupUi(self, MainWindow_main):
        MainWindow_main.setObjectName("MainWindow_main")
        MainWindow_main.resize(1285, 988)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow_main.sizePolicy().hasHeightForWidth())
        MainWindow_main.setSizePolicy(sizePolicy)
        MainWindow_main.setMaximumSize(QtCore.QSize(16777215, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(203, 230, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow_main.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        MainWindow_main.setFont(font)
        MainWindow_main.setStyleSheet("")
        MainWindow_main.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.widget_main = QtWidgets.QWidget(MainWindow_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_main.sizePolicy().hasHeightForWidth())
        self.widget_main.setSizePolicy(sizePolicy)
        self.widget_main.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_main.setAutoFillBackground(False)
        self.widget_main.setStyleSheet("background-color:(255,0,0)")
        self.widget_main.setObjectName("widget_main")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_main)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line_2 = QtWidgets.QFrame(self.widget_main)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.verticalWidget = QtWidgets.QWidget(self.widget_main)
        self.verticalWidget.setMinimumSize(QtCore.QSize(0, 970))
        self.verticalWidget.setMaximumSize(QtCore.QSize(450, 16777215))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_hud = pyG5AIWidget(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_hud.sizePolicy().hasHeightForWidth())
        self.widget_hud.setSizePolicy(sizePolicy)
        self.widget_hud.setMinimumSize(QtCore.QSize(480, 360))
        self.widget_hud.setMaximumSize(QtCore.QSize(480, 360))
        self.widget_hud.setObjectName("widget_hud")
        self.verticalLayout.addWidget(self.widget_hud)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.label_seluav = QtWidgets.QLabel(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.label_seluav.sizePolicy().hasHeightForWidth())
        self.label_seluav.setSizePolicy(sizePolicy)
        self.label_seluav.setMinimumSize(QtCore.QSize(0, 50))
        self.label_seluav.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_seluav.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"color: rgb(0, 0, 0);\n"
"font: 75 20pt \"URW Bookman L\";")
        self.label_seluav.setAlignment(QtCore.Qt.AlignCenter)
        self.label_seluav.setObjectName("label_seluav")
        self.verticalLayout.addWidget(self.label_seluav)
        self.formLayout_3 = QtWidgets.QWidget(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.formLayout_3.sizePolicy().hasHeightForWidth())
        self.formLayout_3.setSizePolicy(sizePolicy)
        self.formLayout_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.formLayout_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.formLayout_3.setStyleSheet("")
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout_5 = QtWidgets.QFormLayout(self.formLayout_3)
        self.formLayout_5.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_5.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_5.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout_5.setHorizontalSpacing(50)
        self.formLayout_5.setObjectName("formLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(114, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(0, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.lcdNumber_altitude = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_altitude.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_altitude.setFont(font)
        self.lcdNumber_altitude.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_altitude.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 14pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_altitude.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_altitude.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_altitude.setSmallDecimalPoint(False)
        self.lcdNumber_altitude.setDigitCount(3)
        self.lcdNumber_altitude.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_altitude.setObjectName("lcdNumber_altitude")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lcdNumber_altitude)
        self.lcdNumber_vspeed = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_vspeed.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_vspeed.setFont(font)
        self.lcdNumber_vspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_vspeed.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 14pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_vspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_vspeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_vspeed.setSmallDecimalPoint(False)
        self.lcdNumber_vspeed.setDigitCount(3)
        self.lcdNumber_vspeed.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_vspeed.setObjectName("lcdNumber_vspeed")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_vspeed)
        self.label_altitude = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_altitude.sizePolicy().hasHeightForWidth())
        self.label_altitude.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_altitude.setFont(font)
        self.label_altitude.setStatusTip("")
        self.label_altitude.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_altitude.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_altitude.setAlignment(QtCore.Qt.AlignCenter)
        self.label_altitude.setObjectName("label_altitude")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_altitude)
        self.label_vspeed = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_vspeed.sizePolicy().hasHeightForWidth())
        self.label_vspeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_vspeed.setFont(font)
        self.label_vspeed.setStatusTip("")
        self.label_vspeed.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_vspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_vspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_vspeed.setObjectName("label_vspeed")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_vspeed)
        self.lcdNumber_airspeed = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_airspeed.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_airspeed.setFont(font)
        self.lcdNumber_airspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_airspeed.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 14pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_airspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_airspeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_airspeed.setDigitCount(3)
        self.lcdNumber_airspeed.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_airspeed.setObjectName("lcdNumber_airspeed")
        self.formLayout_5.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lcdNumber_airspeed)
        self.lcdNumber_gndspeed = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_gndspeed.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_gndspeed.setFont(font)
        self.lcdNumber_gndspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_gndspeed.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 14pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_gndspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_gndspeed.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_gndspeed.setDigitCount(3)
        self.lcdNumber_gndspeed.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_gndspeed.setObjectName("lcdNumber_gndspeed")
        self.formLayout_5.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_gndspeed)
        self.label_airspeed = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_airspeed.sizePolicy().hasHeightForWidth())
        self.label_airspeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_airspeed.setFont(font)
        self.label_airspeed.setStatusTip("")
        self.label_airspeed.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_airspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_airspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_airspeed.setObjectName("label_airspeed")
        self.formLayout_5.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_airspeed)
        self.label_gndspeed = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_gndspeed.sizePolicy().hasHeightForWidth())
        self.label_gndspeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_gndspeed.setFont(font)
        self.label_gndspeed.setStatusTip("")
        self.label_gndspeed.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_gndspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_gndspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gndspeed.setObjectName("label_gndspeed")
        self.formLayout_5.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.label_gndspeed)
        spacerItem2 = QtWidgets.QSpacerItem(114, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(9, QtWidgets.QFormLayout.FieldRole, spacerItem2)
        self.lcdNumber_voltage = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_voltage.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_voltage.setFont(font)
        self.lcdNumber_voltage.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_voltage.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 14pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_voltage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_voltage.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_voltage.setDigitCount(3)
        self.lcdNumber_voltage.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_voltage.setObjectName("lcdNumber_voltage")
        self.formLayout_5.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.lcdNumber_voltage)
        self.lcdNumber_current = QtWidgets.QLCDNumber(self.formLayout_3)
        self.lcdNumber_current.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lcdNumber_current.setFont(font)
        self.lcdNumber_current.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber_current.setStyleSheet("color: rgb(243, 243, 243);\n"
"font: 75 14pt \"Ubuntu Condensed\";\n"
"background-color: rgb(85, 87, 83);")
        self.lcdNumber_current.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber_current.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_current.setDigitCount(3)
        self.lcdNumber_current.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_current.setObjectName("lcdNumber_current")
        self.formLayout_5.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_current)
        self.label_voltage = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_voltage.sizePolicy().hasHeightForWidth())
        self.label_voltage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_voltage.setFont(font)
        self.label_voltage.setStatusTip("")
        self.label_voltage.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_voltage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_voltage.setAlignment(QtCore.Qt.AlignCenter)
        self.label_voltage.setObjectName("label_voltage")
        self.formLayout_5.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_voltage)
        self.label_current = QtWidgets.QLabel(self.formLayout_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_current.sizePolicy().hasHeightForWidth())
        self.label_current.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_current.setFont(font)
        self.label_current.setStatusTip("")
        self.label_current.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"font: 75 15pt \"Waree\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.label_current.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_current.setAlignment(QtCore.Qt.AlignCenter)
        self.label_current.setObjectName("label_current")
        self.formLayout_5.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.label_current)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(13, QtWidgets.QFormLayout.FieldRole, spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(114, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(8, QtWidgets.QFormLayout.FieldRole, spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem7)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(12, QtWidgets.QFormLayout.FieldRole, spacerItem8)
        self.verticalLayout.addWidget(self.formLayout_3)
        self.line_4 = QtWidgets.QFrame(self.verticalWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.gridlayout_functions = QtWidgets.QWidget(self.verticalWidget)
        self.gridlayout_functions.setMaximumSize(QtCore.QSize(16777215, 90))
        self.gridlayout_functions.setObjectName("gridlayout_functions")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridlayout_functions)
        self.gridLayout_3.setContentsMargins(40, 10, 40, 10)
        self.gridLayout_3.setHorizontalSpacing(50)
        self.gridLayout_3.setVerticalSpacing(10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_tune = QtWidgets.QPushButton(self.gridlayout_functions)
        font = QtGui.QFont()
        font.setFamily("Umpush")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_tune.setFont(font)
        self.pushButton_tune.setStyleSheet("background-color: rgb(48,132,70);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Umpush\";")
        self.pushButton_tune.setObjectName("pushButton_tune")
        self.gridLayout_3.addWidget(self.pushButton_tune, 2, 0, 1, 1)
        self.pushButton_servo = QtWidgets.QPushButton(self.gridlayout_functions)
        self.pushButton_servo.setStyleSheet("background-color: rgb(48,132,70);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Umpush\";")
        self.pushButton_servo.setObjectName("pushButton_servo")
        self.gridLayout_3.addWidget(self.pushButton_servo, 2, 1, 1, 1)
        self.pushButton_sensors = QtWidgets.QPushButton(self.gridlayout_functions)
        self.pushButton_sensors.setStyleSheet("background-color: rgb(48,132,70);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Umpush\";")
        self.pushButton_sensors.setObjectName("pushButton_sensors")
        self.gridLayout_3.addWidget(self.pushButton_sensors, 1, 0, 1, 1)
        self.pushButton_rc = QtWidgets.QPushButton(self.gridlayout_functions)
        self.pushButton_rc.setStyleSheet("background-color: rgb(48,132,70);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Umpush\";")
        self.pushButton_rc.setObjectName("pushButton_rc")
        self.gridLayout_3.addWidget(self.pushButton_rc, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.gridlayout_functions)
        self.line_3 = QtWidgets.QFrame(self.verticalWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalWidget = QtWidgets.QWidget(self.verticalWidget)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(0, 80))
        self.horizontalWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.horizontalWidget.setStyleSheet("background-color: rgb(192, 220, 255);")
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_4.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_4.setSpacing(30)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_RTL = QtWidgets.QPushButton(self.horizontalWidget)
        self.pushButton_RTL.setMinimumSize(QtCore.QSize(90, 50))
        self.pushButton_RTL.setStyleSheet("background-color: rgb(187,30,16);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Padauk Book [PYRS]\";")
        self.pushButton_RTL.setObjectName("pushButton_RTL")
        self.horizontalLayout_4.addWidget(self.pushButton_RTL)
        self.pushButton_engineOff = QtWidgets.QPushButton(self.horizontalWidget)
        self.pushButton_engineOff.setMinimumSize(QtCore.QSize(150, 50))
        self.pushButton_engineOff.setStyleSheet("background-color: rgb(187,30,16);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Padauk Book [PYRS]\";")
        self.pushButton_engineOff.setObjectName("pushButton_engineOff")
        self.horizontalLayout_4.addWidget(self.pushButton_engineOff)
        self.pushButton_disarm = QtWidgets.QPushButton(self.horizontalWidget)
        self.pushButton_disarm.setMinimumSize(QtCore.QSize(90, 50))
        self.pushButton_disarm.setStyleSheet("background-color: rgb(187,30,16);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Padauk Book [PYRS]\";")
        self.pushButton_disarm.setObjectName("pushButton_disarm")
        self.horizontalLayout_4.addWidget(self.pushButton_disarm)
        self.verticalLayout.addWidget(self.horizontalWidget)
        self.verticalLayout.setStretch(0, 1)
        self.horizontalLayout_2.addWidget(self.verticalWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_map = MapWidget(self.widget_main)
        self.widget_map.setObjectName("widget_map")
        self.verticalLayout_2.addWidget(self.widget_map)
        self.line = QtWidgets.QFrame(self.widget_main)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_addvehicle = QtWidgets.QPushButton(self.widget_main)
        self.pushButton_addvehicle.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_addvehicle.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Umpush")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_addvehicle.setFont(font)
        self.pushButton_addvehicle.setStyleSheet("background-color: rgb(48,132,70);\n"
"color: rgb(255, 255, 255);\n"
"font: 14pt \"Umpush\";")
        self.pushButton_addvehicle.setObjectName("pushButton_addvehicle")
        self.horizontalLayout.addWidget(self.pushButton_addvehicle)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.widget_main)
        self.tableWidget.setMinimumSize(QtCore.QSize(800, 100))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setKerning(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("background-color: rgb(203, 230, 255);")
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 1)
        MainWindow_main.setCentralWidget(self.widget_main)

        self.retranslateUi(MainWindow_main)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_main)

    def retranslateUi(self, MainWindow_main):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_main.setWindowTitle(_translate("MainWindow_main", "MainWindow"))
        self.widget_main.setToolTip(_translate("MainWindow_main", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_seluav.setText(_translate("MainWindow_main", "Current DRONE NAME"))
        self.label_altitude.setText(_translate("MainWindow_main", "Altitude"))
        self.label_vspeed.setText(_translate("MainWindow_main", "V. Speed"))
        self.label_airspeed.setText(_translate("MainWindow_main", "Airspeed"))
        self.label_gndspeed.setText(_translate("MainWindow_main", "Gnd. Speed"))
        self.label_voltage.setText(_translate("MainWindow_main", "Voltage"))
        self.label_current.setText(_translate("MainWindow_main", "Current"))
        self.pushButton_tune.setText(_translate("MainWindow_main", "Tune Parameters"))
        self.pushButton_servo.setText(_translate("MainWindow_main", "Servo Channels"))
        self.pushButton_sensors.setText(_translate("MainWindow_main", "Sensors"))
        self.pushButton_rc.setText(_translate("MainWindow_main", "RC Channels"))
        self.pushButton_RTL.setText(_translate("MainWindow_main", "RTL"))
        self.pushButton_engineOff.setText(_translate("MainWindow_main", "Engine OFF"))
        self.pushButton_disarm.setText(_translate("MainWindow_main", "Disarm"))
        self.pushButton_addvehicle.setText(_translate("MainWindow_main", "Add a Vehicle"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_main", "VEHICLE"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow_main", "MODE"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow_main", "FLYING TO"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow_main", "TIME IN AIR"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow_main", "ALTITUDE"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow_main", "VOLTAGE"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow_main", "CURRENT"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow_main", "RELAY"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow_main", "ENGINE"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow_main", "DISCONNECT"))
from gust.gui.ui.attitude_ind_widget import pyG5AIWidget
from gust.gui.ui.map_widget import MapWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow_main = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_main()
    ui.setupUi(MainWindow_main)
    MainWindow_main.show()
    sys.exit(app.exec_())
