"""Logic for sensor selection window."""
from PyQt5.QtWidgets import QMainWindow
from gust.gui.ui.sensors import Ui_SensorsWindow

class SensorsWindow(QMainWindow, Ui_SensorsWindow):
    """Main interface for the sensors selection window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.ctx = ctx
        self._zed_window = None

        self.pushButton_zed.clicked.connect(self.zed_clicked)


    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)
        self.setPalette(self.parentWidget().palette())

    def zed_clicked(self):
        pass

        # Open up the ZED interface window

        # self._zed_window = ZedWindow(self.ctx, parent=self.parent())
        # self._zed_window.show()
        # self.close()
