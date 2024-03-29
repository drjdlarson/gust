"""Logic for Flight Planning scheme selection"""
from PyQt5.QtWidgets import QMessageBox, QDialog, QMainWindow
from gust.gui.ui.planning_module import Ui_MainWindow
from gust.gui import cmr_window, general_planning_window

PLANNING_TYPES = ["General Planning", "CMR Planning"]


class PlanningSelectionWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the planning selection window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.ctx = ctx

        self._cmrWindow = None
        self._generalWindow = None

        self.comboBox_planning_types.addItems(PLANNING_TYPES)
        self.pushButton_open.clicked.connect(self.clicked_open)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)

    def clicked_cancel(self):
        self.close()

    def clicked_open(self):
        """Opens the selected planning window"""
        # Currently only includes CMR Planning Window

        sel_type = self.comboBox_planning_types.currentText()
        if sel_type == "CMR Planning":
            if self._cmrWindow is None:
                self._cmrWindow = cmr_window.CmrWindow(self.ctx, parent=self)
            self._cmrWindow.show()
        elif sel_type == "General Planning":
            if self._generalWindow is None:
                self._generalWindow = general_planning_window.GeneralPlanningWindow(
                    self.ctx, parent=self
                )
            self._generalWindow.show()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.setPalette(self.parentWidget().palette())
