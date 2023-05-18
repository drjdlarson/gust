"""Logic for RTL confirmation window"""
from gust.gui.ui.confirmation import Ui_MainWindow
from PyQt5.QtWidgets import QDialog


class RTLConfirmation(QDialog, Ui_MainWindow):
    """Main interface for the confirmation window before disconnecting"""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.label_custom.setText("Activate RTL?")

    def clicked_ok(self):
        # Currently not connected to anything
        # This just needs to send a URL request to change flight mode
        # Similar to as in commands_window.py
        self.reject()

    def clicked_cancel(self):
        self.reject()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
