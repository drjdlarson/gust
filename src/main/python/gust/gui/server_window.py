import sys
from time import sleep
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

from gust.gui.ui.server_window import Ui_ServerWindow
import gust.server as server
import gust.server.settings as settings


class ServerWindow(QMainWindow, Ui_ServerWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.lineEdit_port.setValidator(QIntValidator())

        settings.PORT = int(self.lineEdit_port.text())
        settings.IP = self.lineEdit_IP.text()

        # connect buttons
        self.pushButton_start.clicked.connect(self.clicked_start)
        self.pushButton_stop.clicked.connect(self.clicked_stop)
        self.lineEdit_IP.textChanged.connect(self.changed_ip)
        self.lineEdit_port.textChanged.connect(self.changed_port)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

    def _stop_server(self):
        if server.stop_server():
            self.update_console_text()

            msg = '---------------- Stopping Server Process -----------------'
            self.textEdit_output.append(msg)

    @pyqtSlot()
    def update_console_text(self):
        outputBytes = server.SERVER_PROC.readAll().data()
        outputUnicode = outputBytes.decode('utf-8')
        self.textEdit_output.append( outputUnicode )

    @pyqtSlot()
    def clicked_start(self):
        msg = '---------------- Starting Server Process -----------------'
        self.textEdit_output.append(msg)

        res, err = server.start_server()

        self.textEdit_output.append(server.START_CMD)
        self.textEdit_output.append('\n')

        if res:
            server.SERVER_PROC.readyReadStandardOutput.connect(self.update_console_text)

        else:
            msg = 'FAILED TO START SERVER:\n{:s}'.format(err)
            self.textEdit_output.append(msg)

    @pyqtSlot()
    def clicked_stop(self):
        self._stop_server()

    @pyqtSlot(str)
    def changed_ip(self, text):
        settings.IP = text

    @pyqtSlot(str)
    def changed_port(self, text):
        settings.PORT = int(text)

    def closeEvent(self, event):
        # nicely close all
        self._stop_server()

        sys.stdout.flush()
        sys.stderr.flush()
        sleep(0.25)
