"""Logic for flight log analyzer window"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from gust.gui.ui.log import Ui_MainWindow

URL_BASE="http://localhost:8000/api/"

class LogWindow(QMainWindow,Ui_MainWindow):
    """Main interface for the flight log analyzing window"""

    # Currently not connected to anything.
    # This window should accept flight log data from connected vehicles via MAVLink
    # and be able to do the following:
    # 1. Create an interface to visualize the data (plot time data based on selection)
    # 2. Save the log data in certain formats for future use.

    def __init__(self,ctx):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
