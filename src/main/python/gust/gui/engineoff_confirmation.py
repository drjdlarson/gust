"""Logic for engine-off confirmation window."""
from PyQt5.QtWidgets import QDialog
from gust.gui.ui.confirmation import Ui_MainWindow

URL_BASE = "http://localhost:8000/api/"


class EngineOffConfirmation(QDialog, Ui_MainWindow):
    """Main interface for the confirmation window before disconnecting"""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        # event connections
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.label_custom.setText("Engine Shutdown?")

    def clicked_ok(self):
        """Currently not doing anything, needs to request signal for engine-off"""
        self.reject()

    def clicked_cancel(self):
        """Closes the disconnect confirmation window"""
        self.reject()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
