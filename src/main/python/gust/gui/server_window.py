import sys
from time import sleep
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QIntValidator

from gust.gui.ui.server_window import Ui_ServerWindow
import gust.server.server as server
import gust.server.settings as settings
from gust.plugins.plugin_monitor import pluginMonitor


class ServerWindow(QMainWindow, Ui_ServerWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._scan_plugins()

        self.lineEdit_port.setValidator(QIntValidator())

        settings.PORT = int(self.lineEdit_port.text())
        settings.IP = self.lineEdit_IP.text()


        # connect buttons
        self.pushButton_plugScan.clicked.connect(self.clicked_plugScan)
        self.pushButton_start.clicked.connect(self.clicked_start)
        self.pushButton_stop.clicked.connect(self.clicked_stop)
        self.lineEdit_IP.textChanged.connect(self.changed_ip)
        self.lineEdit_port.textChanged.connect(self.changed_port)

    def _scan_plugins(self):
        pluginMonitor.scan_for_plugins()

        self.listWidget_availPlugins.clear()
        self.listWidget_selPlugins.clear()
        for plugin in pluginMonitor.avail_plugins:
            self.listWidget_availPlugins.addItem(plugin)

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

    def _stop_server(self):
        succ = server.stop_server()
        if not succ:
            msg = ('[server] Failed to stop server.')
            self.textEdit_output.append(msg)

        return succ

    def _stop_plug_mon(self):
        succ = pluginMonitor.stop_monitor()
        if not succ:
            msg = ('[plugin-monitor] Failed to stop plugin-monitor.')
            self.textEdit_output.append(msg)

        return succ

    def _stop_subtasks(self):
        succ = self._stop_server()
        succ = self._stop_plug_mon() and succ

        return succ

    @pyqtSlot()
    def update_console_text(self):
        outputBytes = server.SERVER_PROC.readAll().data()
        outputUnicode = outputBytes.decode('utf-8')
        self.textEdit_output.append(outputUnicode)

    @pyqtSlot()
    def clicked_plugScan(self):
        self._scan_plugins()

    @pyqtSlot()
    def clicked_start(self):
        msg = ('----------------------------------------------------------\n'
               + '------------------- Starting Backend ---------------------\n'
               + '----------------------------------------------------------')
        self.textEdit_output.append(msg)

        res, err = server.start_server()

        self.textEdit_output.append('[server] {:s}'.format(server.START_CMD))
        self.textEdit_output.append('\n')

        if res:
            server.SERVER_PROC.readyReadStandardOutput.connect(self.update_console_text)

        else:
            msg = '[server] FAILED TO START SERVER:\n{:s}'.format(err)
            self.textEdit_output.append(msg)

        self.textEdit_output.append('[plugin-monitor] Scanning for plugins')
        pluginMonitor.scan_for_plugins()

        self.textEdit_output.append('[plugin-monitor] Starting monitor')
        pluginMonitor.start_monitor()

    @pyqtSlot()
    def clicked_stop(self):
        succ = self._stop_subtasks()

        if succ:
            msg = ('----------------------------------------------------------\n'
                  + '------------------- Stopping Backend ---------------------\n'
                  + '----------------------------------------------------------\n')
            self.textEdit_output.append(msg)

    @pyqtSlot(str)
    def changed_ip(self, text):
        settings.IP = text

    @pyqtSlot(str)
    def changed_port(self, text):
        settings.PORT = int(text)

    def closeEvent(self, event):
        # nicely close all
        self._stop_subtasks()

        sys.stdout.flush()
        sys.stderr.flush()
