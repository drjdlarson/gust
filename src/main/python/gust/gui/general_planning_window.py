"""Logic for General Planning Window"""

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QPushButton,
    QComboBox,
)

from gust.gui.ui.general_planning import Ui_MainWindow
from wsgi_apps.api.url_bases import BASE, DRONE

class GeneralPlanningWindow(QMainWindow, Ui_MainWindow):
    """Main Interface for general planning window."""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx
        self.setupUi(self)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

        self.widget_planning_map.setup_qml(self.ctx)

