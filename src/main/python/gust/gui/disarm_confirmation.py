"""Logic for Disarm Confirmation window"""

from PyQt5.QtWidgets import QDialog
from gust.gui.ui.confirmation import Ui_MainWindow


class DisarmConfirmation(QDialog, Ui_MainWindow):
    """Main interface for the confirmation window before disconnecting"""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        # event connections
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.label_custom.setText("Disarm?")

    def clicked_ok(self):
        """Currently not doing anything, Need to connect this to disarm request."""
        self.reject()

    def clicked_cancel(self):
        """Close the disarm confirmation window"""
        self.reject()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
