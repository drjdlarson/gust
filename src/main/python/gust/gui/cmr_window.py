"""Logic for CMR planning window"""
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

from gust.gui.ui.cmr_window import Ui_MainWindow

class CmrWindow(QMainWindow, Ui_MainWindow):
    """Main interface for the CMR Planning window"""

    def __init__(self, ctx, parent=None):
        super().__init__(parent=parent)

        self.ctx = ctx
        print("opening cmr window")
        self.setupUi(self)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.setPalette(self.parentWidget().palette())

        pixmap = QPixmap(self.ctx.get_resource('cmr_planning/cmr_schematic.jpeg'))
        self.label_schematic.setPixmap(pixmap)

        self.widget_cmr_map.setup_qml(self.ctx)
