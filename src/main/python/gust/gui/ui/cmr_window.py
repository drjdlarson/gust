# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/gust/gui/ui/cmr_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(988, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_cmr_map = PlanningMapWidget(self.centralwidget)
        self.widget_cmr_map.setMinimumSize(QtCore.QSize(680, 400))
        self.widget_cmr_map.setObjectName("widget_cmr_map")
        self.verticalLayout.addWidget(self.widget_cmr_map)
        self.horizontalLayout_checkboxes = QtWidgets.QHBoxLayout()
        self.horizontalLayout_checkboxes.setObjectName("horizontalLayout_checkboxes")
        self.checkBox_grid = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_grid.setObjectName("checkBox_grid")
        self.horizontalLayout_checkboxes.addWidget(self.checkBox_grid)
        self.checkBox_waypoints = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_waypoints.setObjectName("checkBox_waypoints")
        self.horizontalLayout_checkboxes.addWidget(self.checkBox_waypoints)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_checkboxes.addItem(spacerItem)
        self.pushButton_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.horizontalLayout_checkboxes.addWidget(self.pushButton_refresh)
        self.verticalLayout.addLayout(self.horizontalLayout_checkboxes)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.tableWidget_drones = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_drones.setShowGrid(True)
        self.tableWidget_drones.setRowCount(2)
        self.tableWidget_drones.setColumnCount(4)
        self.tableWidget_drones.setObjectName("tableWidget_drones")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_drones.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_drones.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_drones.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_drones.setHorizontalHeaderItem(3, item)
        self.tableWidget_drones.horizontalHeader().setVisible(True)
        self.tableWidget_drones.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_drones.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_drones.horizontalHeader().setMinimumSectionSize(60)
        self.tableWidget_drones.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_drones.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_drones.verticalHeader().setVisible(True)
        self.tableWidget_drones.verticalHeader().setHighlightSections(True)
        self.tableWidget_drones.verticalHeader().setMinimumSectionSize(20)
        self.tableWidget_drones.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget_drones)
        self.verticalLayout.setStretch(0, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_2.addWidget(self.line_6)
        self.label_grid_planning = QtWidgets.QLabel(self.centralwidget)
        self.label_grid_planning.setAlignment(QtCore.Qt.AlignCenter)
        self.label_grid_planning.setObjectName("label_grid_planning")
        self.verticalLayout_2.addWidget(self.label_grid_planning)
        self.formLayout_grid_planning = QtWidgets.QFormLayout()
        self.formLayout_grid_planning.setObjectName("formLayout_grid_planning")
        self.lineEdit_grid_spacing = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_grid_spacing.setReadOnly(False)
        self.lineEdit_grid_spacing.setObjectName("lineEdit_grid_spacing")
        self.formLayout_grid_planning.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lineEdit_grid_spacing)
        self.label_grid_spacing = QtWidgets.QLabel(self.centralwidget)
        self.label_grid_spacing.setObjectName("label_grid_spacing")
        self.formLayout_grid_planning.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_grid_spacing)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout_grid_planning.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_start_lat = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_start_lat.setObjectName("lineEdit_start_lat")
        self.formLayout_grid_planning.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lineEdit_start_lat)
        self.lineEdit_start_lon = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_start_lon.sizePolicy().hasHeightForWidth())
        self.lineEdit_start_lon.setSizePolicy(sizePolicy)
        self.lineEdit_start_lon.setObjectName("lineEdit_start_lon")
        self.formLayout_grid_planning.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lineEdit_start_lon)
        self.lineEdit_end_lat = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_end_lat.setObjectName("lineEdit_end_lat")
        self.formLayout_grid_planning.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lineEdit_end_lat)
        self.lineEdit_end_lon = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_end_lon.sizePolicy().hasHeightForWidth())
        self.lineEdit_end_lon.setSizePolicy(sizePolicy)
        self.lineEdit_end_lon.setObjectName("lineEdit_end_lon")
        self.formLayout_grid_planning.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lineEdit_end_lon)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout_grid_planning.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout_grid_planning.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_grid_planning.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout_grid_planning.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.label_5)
        self.verticalLayout_2.addLayout(self.formLayout_grid_planning)
        self.pushButton_draw_grid = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw_grid.setObjectName("pushButton_draw_grid")
        self.verticalLayout_2.addWidget(self.pushButton_draw_grid)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_2.addWidget(self.line_5)
        self.label_cmr_planning = QtWidgets.QLabel(self.centralwidget)
        self.label_cmr_planning.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cmr_planning.setObjectName("label_cmr_planning")
        self.verticalLayout_2.addWidget(self.label_cmr_planning)
        self.formLayout_cmr_planning = QtWidgets.QFormLayout()
        self.formLayout_cmr_planning.setObjectName("formLayout_cmr_planning")
        self.lineEdit_rel_height = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_rel_height.setObjectName("lineEdit_rel_height")
        self.formLayout_cmr_planning.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lineEdit_rel_height)
        self.label_rel_height = QtWidgets.QLabel(self.centralwidget)
        self.label_rel_height.setObjectName("label_rel_height")
        self.formLayout_cmr_planning.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_rel_height)
        self.lineEdit_spacing = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_spacing.setObjectName("lineEdit_spacing")
        self.formLayout_cmr_planning.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lineEdit_spacing)
        self.label_spacing = QtWidgets.QLabel(self.centralwidget)
        self.label_spacing.setObjectName("label_spacing")
        self.formLayout_cmr_planning.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_spacing)
        self.lineEdit_theta_max = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_theta_max.setObjectName("lineEdit_theta_max")
        self.formLayout_cmr_planning.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lineEdit_theta_max)
        self.label_theta_max = QtWidgets.QLabel(self.centralwidget)
        self.label_theta_max.setObjectName("label_theta_max")
        self.formLayout_cmr_planning.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_theta_max)
        self.lineEdit_theta_min = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_theta_min.setObjectName("lineEdit_theta_min")
        self.formLayout_cmr_planning.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lineEdit_theta_min)
        self.label_theta_min = QtWidgets.QLabel(self.centralwidget)
        self.label_theta_min.setObjectName("label_theta_min")
        self.formLayout_cmr_planning.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_theta_min)
        self.verticalLayout_2.addLayout(self.formLayout_cmr_planning)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_load_wp = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_load_wp.setObjectName("pushButton_load_wp")
        self.horizontalLayout.addWidget(self.pushButton_load_wp)
        self.pushButton_generate_wp = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_generate_wp.setObjectName("pushButton_generate_wp")
        self.horizontalLayout.addWidget(self.pushButton_generate_wp)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_2.addWidget(self.line_7)
        self.pushButton_start_cmr = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_cmr.setObjectName("pushButton_start_cmr")
        self.verticalLayout_2.addWidget(self.pushButton_start_cmr)
        self.pushButton_stop_cmr = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop_cmr.setObjectName("pushButton_stop_cmr")
        self.verticalLayout_2.addWidget(self.pushButton_stop_cmr)
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.verticalLayout_2.addWidget(self.line_9)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.pushButton_test_upload_waypoints = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_upload_waypoints.setObjectName("pushButton_test_upload_waypoints")
        self.verticalLayout_2.addWidget(self.pushButton_test_upload_waypoints)
        self.pushButton_test_goto_next = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_goto_next.setObjectName("pushButton_test_goto_next")
        self.verticalLayout_2.addWidget(self.pushButton_test_goto_next)
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_2.addWidget(self.line_8)
        self.label_schematic = QtWidgets.QLabel(self.centralwidget)
        self.label_schematic.setMinimumSize(QtCore.QSize(0, 200))
        self.label_schematic.setText("")
        self.label_schematic.setObjectName("label_schematic")
        self.verticalLayout_2.addWidget(self.label_schematic)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox_grid.setText(_translate("MainWindow", "Grid"))
        self.checkBox_waypoints.setText(_translate("MainWindow", "Waypoints"))
        self.pushButton_refresh.setText(_translate("MainWindow", "Refresh"))
        item = self.tableWidget_drones.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "DRONE_COLOR"))
        item = self.tableWidget_drones.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "DRONE_NAME"))
        item = self.tableWidget_drones.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "WAYPOINTS"))
        item = self.tableWidget_drones.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "UPLOAD"))
        self.label_grid_planning.setText(_translate("MainWindow", "Grid Planning"))
        self.label_grid_spacing.setText(_translate("MainWindow", "Grid Spacing (m)"))
        self.label_3.setText(_translate("MainWindow", "FOR SINGLE LINE::"))
        self.label.setText(_translate("MainWindow", "Start Latitude"))
        self.label_2.setText(_translate("MainWindow", "Start Longitude"))
        self.label_4.setText(_translate("MainWindow", "End Latitude"))
        self.label_5.setText(_translate("MainWindow", "End Longitude"))
        self.pushButton_draw_grid.setText(_translate("MainWindow", "Draw Grid"))
        self.label_cmr_planning.setText(_translate("MainWindow", "CMR Planning"))
        self.label_rel_height.setText(_translate("MainWindow", "<html><head/><body><p>Rel. Height H (m)</p></body></html>"))
        self.label_spacing.setText(_translate("MainWindow", "Spacing (m)"))
        self.label_theta_max.setText(_translate("MainWindow", "<html><head/><body><p>Max. θ</p></body></html>"))
        self.label_theta_min.setText(_translate("MainWindow", "<html><head/><body><p>Min. θ</p></body></html>"))
        self.pushButton_load_wp.setText(_translate("MainWindow", "Load Waypoints"))
        self.pushButton_generate_wp.setText(_translate("MainWindow", "Generate Waypoints"))
        self.pushButton_start_cmr.setText(_translate("MainWindow", "Start CMR operation"))
        self.pushButton_stop_cmr.setText(_translate("MainWindow", "Stop CMR operation"))
        self.pushButton_test_upload_waypoints.setText(_translate("MainWindow", "TEST-upload waypoints"))
        self.pushButton_test_goto_next.setText(_translate("MainWindow", "TEST-goto_next"))
from gust.gui.ui.planning_map_widget import PlanningMapWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
